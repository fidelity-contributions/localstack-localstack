# > In API Gateway, an API's method request or response can take a payload in a different format from the integration
# request or response.
#
# You can transform your data to:
# - Match the payload to an API-specified format.
# - Override an API's request and response parameters and status codes.
# - Return client selected response headers.
# - Associate path parameters, query string parameters, or header parameters in the method request of HTTP proxy
#       or AWS service proxy. TODO: this is from the documentation. Can we use requestOverides for proxy integrations?
# - Select which data to send using integration with AWS services, such as Amazon DynamoDB or Lambda functions,
#       or HTTP endpoints.
#
# You can use mapping templates to transform your data. A mapping template is a script expressed in Velocity Template
# Language (VTL) and applied to the payload using JSONPath .
#
# https://docs.aws.amazon.com/apigateway/latest/developerguide/models-mappings.html
import base64
import copy
import json
import logging
from typing import Any, TypedDict
from urllib.parse import quote_plus, unquote_plus

import airspeed
from airspeed.operators import dict_to_string
from jsonpath_rw import parse

from localstack import config
from localstack.services.apigateway.next_gen.execute_api.variables import (
    ContextVariableOverrides,
    ContextVariables,
    ContextVarsResponseOverride,
)
from localstack.utils.aws.templating import APIGW_SOURCE, VelocityUtil, VtlTemplate
from localstack.utils.json import json_safe

LOG = logging.getLogger(__name__)


class MappingTemplateParams(TypedDict, total=False):
    path: dict[str, str]
    querystring: dict[str, str]
    header: dict[str, str]


class MappingTemplateInput(TypedDict, total=False):
    body: str
    params: MappingTemplateParams


class MappingTemplateVariables(TypedDict, total=False):
    context: ContextVariables
    input: MappingTemplateInput
    stageVariables: dict[str, str]


def cast_to_vtl_object(value):
    if isinstance(value, dict):
        return VTLMap(value)
    if isinstance(value, list):
        return [cast_to_vtl_object(item) for item in value]
    return value


def cast_to_vtl_json_object(value: Any) -> Any:
    if isinstance(value, dict):
        return VTLJsonDict(value)
    if isinstance(value, list):
        return VTLJsonList(value)
    return value


def extract_jsonpath(value: dict | list, path: str):
    jsonpath_expr = parse(path)
    result = [match.value for match in jsonpath_expr.find(value)]
    if not result:
        return None
    result = result[0] if len(result) == 1 else result
    return result


class VTLMap(dict):
    """Overrides __str__ of python dict (and all child dict) to return a Java like string representation"""

    # TODO apply this class more generally through the template mappings

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update(*args, **kwargs)

    @staticmethod
    def cast_factory(value: Any) -> Any:
        return cast_to_vtl_object(value)

    def update(self, *args, **kwargs):
        for k, v in self.items():
            self[k] = self.cast_factory(v)

    def __str__(self) -> str:
        return dict_to_string(self)


class VTLJsonList(list):
    """Some VTL List behave differently when being represented as string and everything
    inside will be represented as a json string

    Example: $input.path('$').b // Where path is {"a": 1, "b": [{"c": 5}]}
    Results: '[{"c":5}]' // Where everything inside the list is a valid json object
    """

    def __init__(self, *args):
        super(VTLJsonList, self).__init__(*args)
        for idx, item in enumerate(self):
            self[idx] = cast_to_vtl_json_object(item)

    def __str__(self):
        if isinstance(self, list):
            return json.dumps(self, separators=(",", ":"))


class VTLJsonDict(VTLMap):
    """Some VTL Map behave differently when being represented as string and a list
    encountered in the dictionary will be represented as a json string

    Example: $input.path('$') // Where path is {"a": 1, "b": [{"c": 5}]}
    Results: '{a=1, b=[{"c":5}]}' // Where everything inside the list is a valid json object
    """

    @staticmethod
    def cast_factory(value: Any) -> Any:
        return cast_to_vtl_json_object(value)


class AttributeDict(dict):
    """
    Wrapper returned by VelocityUtilApiGateway.parseJson to allow access to dict values as attributes (dot notation),
    e.g.: $util.parseJson('$.foo').bar
    """

    def __init__(self, *args, **kwargs):
        super(AttributeDict, self).__init__(*args, **kwargs)
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = AttributeDict(value)

    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError(f"'AttributeDict' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError(f"'AttributeDict' object has no attribute '{name}'")


class VelocityUtilApiGateway(VelocityUtil):
    """
    Simple class to mimic the behavior of variable '$util' in AWS API Gateway integration
    velocity templates.
    See: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html
    """

    def base64Encode(self, s):
        if not isinstance(s, str):
            s = json.dumps(s)
        encoded_str = s.encode(config.DEFAULT_ENCODING)
        encoded_b64_str = base64.b64encode(encoded_str)
        return encoded_b64_str.decode(config.DEFAULT_ENCODING)

    def base64Decode(self, s):
        if not isinstance(s, str):
            s = json.dumps(s)
        return base64.b64decode(s)

    def toJson(self, obj):
        return obj and json.dumps(obj)

    def urlEncode(self, s):
        return quote_plus(s)

    def urlDecode(self, s):
        return unquote_plus(s)

    def escapeJavaScript(self, obj: Any) -> str:
        """
        Converts the given object to a string and escapes any regular single quotes (') into escaped ones (\').
        JSON dumps will escape the single quotes.
        https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html
        """
        if obj is None:
            return "null"
        if isinstance(obj, str):
            # empty string escapes to empty object
            if len(obj.strip()) == 0:
                return "{}"
            return json.dumps(obj)[1:-1]
        if obj in (True, False):
            return str(obj).lower()
        return str(obj)

    def parseJson(self, s: str):
        obj = json.loads(s)
        return AttributeDict(obj) if isinstance(obj, dict) else obj


class VelocityInput:
    """
    Simple class to mimic the behavior of variable '$input' in AWS API Gateway integration
    velocity templates.
    See: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html
    """

    def __init__(self, body, params):
        self.parameters = params or {}
        self.value = body

    def _extract_json_path(self, path):
        if not self.value:
            return None
        if isinstance(self.value, dict):
            value = self.value
        else:
            try:
                value = json.loads(self.value)
            except json.JSONDecodeError:
                return None

        return extract_jsonpath(value, path)

    def path(self, path):
        return cast_to_vtl_json_object(self._extract_json_path(path))

    def json(self, path):
        path = path or "$"
        matching = self._extract_json_path(path)
        if matching is None:
            matching = ""
        elif isinstance(matching, (list, dict)):
            matching = json_safe(matching)
        return json.dumps(matching)

    @property
    def body(self):
        if not self.value:
            return "{}"

        return self.value

    def params(self, name=None):
        if not name:
            return self.parameters
        for k in ["path", "querystring", "header"]:
            if val := self.parameters.get(k).get(name):
                return val
        return ""

    def __getattr__(self, name):
        return self.value.get(name)

    def __repr__(self):
        return "$input"


class ApiGatewayVtlTemplate(VtlTemplate):
    """Util class for rendering VTL templates with API Gateway specific extensions"""

    def prepare_namespace(self, variables, source: str = APIGW_SOURCE) -> dict[str, Any]:
        namespace = super().prepare_namespace(variables, source)
        input_var = variables.get("input") or {}
        variables = {
            "input": VelocityInput(input_var.get("body"), input_var.get("params")),
            "util": VelocityUtilApiGateway(),
        }
        namespace.update(variables)
        return namespace

    def render_request(
        self,
        template: str,
        variables: MappingTemplateVariables,
        context_overrides: ContextVariableOverrides,
    ) -> tuple[str, ContextVariableOverrides]:
        variables_copy: MappingTemplateVariables = copy.deepcopy(variables)
        variables_copy["context"].update(copy.deepcopy(context_overrides))
        result = self.render_vtl(template=template.strip(), variables=variables_copy)
        return result, ContextVariableOverrides(
            requestOverride=variables_copy["context"]["requestOverride"],
            responseOverride=variables_copy["context"]["responseOverride"],
        )

    def render_response(
        self,
        template: str,
        variables: MappingTemplateVariables,
        context_overrides: ContextVariableOverrides,
    ) -> tuple[str, ContextVarsResponseOverride]:
        variables_copy: MappingTemplateVariables = copy.deepcopy(variables)
        variables_copy["context"].update(copy.deepcopy(context_overrides))
        result = self.render_vtl(template=template.strip(), variables=variables_copy)
        return result, variables_copy["context"]["responseOverride"]


# patches required to allow our custom class operations in VTL templates processed by airspeed
airspeed.operators.__additional_methods__[VTLMap] = airspeed.operators.__additional_methods__[dict]
airspeed.operators.__additional_methods__[VTLJsonDict] = airspeed.operators.__additional_methods__[
    dict
]
airspeed.operators.__additional_methods__[VTLJsonList] = airspeed.operators.__additional_methods__[
    list
]
