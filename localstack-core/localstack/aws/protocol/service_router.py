import logging
from typing import NamedTuple, Optional, Set

from botocore.model import ServiceModel
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.http import parse_dict_header

from localstack.aws.spec import (
    ServiceCatalog,
    ServiceModelIdentifier,
    get_service_catalog,
)
from localstack.http import Request
from localstack.services.s3.utils import uses_host_addressing
from localstack.services.sqs.utils import is_sqs_queue_url
from localstack.utils.strings import to_bytes

LOG = logging.getLogger(__name__)


class _ServiceIndicators(NamedTuple):
    """
    Encapsulates the different fields that might indicate which service a request is targeting.

    This class does _not_ contain any data which is parsed from the body of the request in order to defer or even avoid
    processing the body.
    """

    # AWS service's "signing name" - Contained in the Authorization header
    # (https://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-auth-using-authorization-header.html)
    signing_name: Optional[str] = None
    # Target prefix as defined in the service specs for non-rest protocols - Contained in the X-Amz-Target header
    target_prefix: Optional[str] = None
    # Targeted operation as defined in the service specs for non-rest protocols - Contained in the X-Amz-Target header
    operation: Optional[str] = None
    # Host field of the HTTP request
    host: Optional[str] = None
    # Path of the HTTP request
    path: Optional[str] = None


def _extract_service_indicators(request: Request) -> _ServiceIndicators:
    """Extracts all different fields that might indicate which service a request is targeting."""
    x_amz_target = request.headers.get("x-amz-target")
    authorization = request.headers.get("authorization")

    signing_name = None
    if authorization:
        try:
            auth_type, auth_info = authorization.split(None, 1)
            auth_type = auth_type.lower().strip()
            if auth_type == "aws4-hmac-sha256":
                values = parse_dict_header(auth_info)
                _, _, _, signing_name, _ = values["Credential"].split("/")
        except (ValueError, KeyError):
            LOG.debug("auth header could not be parsed for service routing: %s", authorization)
            pass
    if x_amz_target:
        if "." in x_amz_target:
            target_prefix, operation = x_amz_target.split(".", 1)
        else:
            target_prefix = None
            operation = x_amz_target
    else:
        target_prefix, operation = None, None

    return _ServiceIndicators(signing_name, target_prefix, operation, request.host, request.path)


signing_name_path_prefix_rules = {
    # custom rules based on URI path prefixes that are not easily generalizable
    "apigateway": {
        "/v2": ServiceModelIdentifier("apigatewayv2"),
    },
    "appconfig": {
        "/configuration": ServiceModelIdentifier("appconfigdata"),
    },
    "bedrock": {
        "/guardrail/": ServiceModelIdentifier("bedrock-runtime"),
        "/model/": ServiceModelIdentifier("bedrock-runtime"),
        "/async-invoke": ServiceModelIdentifier("bedrock-runtime"),
    },
    "execute-api": {
        "/@connections": ServiceModelIdentifier("apigatewaymanagementapi"),
        "/participant": ServiceModelIdentifier("connectparticipant"),
        "*": ServiceModelIdentifier("iot"),
    },
    "ses": {
        "/v2": ServiceModelIdentifier("sesv2"),
        "/v1": ServiceModelIdentifier("pinpoint-email"),
    },
    "greengrass": {
        "/greengrass/v2/": ServiceModelIdentifier("greengrassv2"),
    },
    "cloudsearch": {
        "/2013-01-01": ServiceModelIdentifier("cloudsearchdomain"),
    },
    "s3": {"/v20180820": ServiceModelIdentifier("s3control")},
    "iot1click": {
        "/projects": ServiceModelIdentifier("iot1click-projects"),
        "/devices": ServiceModelIdentifier("iot1click-devices"),
    },
    "es": {
        "/2015-01-01": ServiceModelIdentifier("es"),
        "/2021-01-01": ServiceModelIdentifier("opensearch"),
    },
    "sagemaker": {
        "/endpoints": ServiceModelIdentifier("sagemaker-runtime"),
        "/human-loops": ServiceModelIdentifier("sagemaker-a2i-runtime"),
    },
}


def custom_signing_name_rules(signing_name: str, path: str) -> Optional[ServiceModelIdentifier]:
    """
    Rules which are based on the signing name (in the auth header) and the request path.
    """
    rules = signing_name_path_prefix_rules.get(signing_name)

    if not rules:
        if signing_name == "servicecatalog":
            if path == "/":
                # servicecatalog uses the protocol json (only uses root-path URIs, i.e. only /)
                return ServiceModelIdentifier("servicecatalog")
            else:
                # servicecatalog-appregistry uses rest-json (only uses non-root-path request URIs)
                return ServiceModelIdentifier("servicecatalog-appregistry")
        return

    for prefix, service_model_identifier in rules.items():
        if path.startswith(prefix):
            return service_model_identifier

    return rules.get("*", ServiceModelIdentifier(signing_name))


def custom_host_addressing_rules(host: str) -> Optional[ServiceModelIdentifier]:
    """
    Rules based on the host header of the request, which is typically the data plane of a service.

    Some services are added through a patch in ext.
    """
    if ".lambda-url." in host:
        return ServiceModelIdentifier("lambda")

    if ".s3-website." in host:
        return ServiceModelIdentifier("s3")


def custom_path_addressing_rules(path: str) -> Optional[ServiceModelIdentifier]:
    """
    Rules which are only based on the request path.
    """

    if is_sqs_queue_url(path):
        return ServiceModelIdentifier("sqs", protocol="query")

    if path.startswith("/2015-03-31/functions"):
        return ServiceModelIdentifier("lambda")


def legacy_s3_rules(request: Request) -> Optional[ServiceModelIdentifier]:
    """
    *Legacy* rules which allow us to fallback to S3 if no other service was matched.
    All rules which are implemented here should be removed once we make sure it would not break any use-cases.
    """

    path = request.path
    method = request.method

    # TODO The remaining rules here are special S3 rules - needs to be discussed how these should be handled.
    #      Some are similar to other rules and not that greedy, others are nearly general fallbacks.
    stripped = path.strip("/")
    if method in ["GET", "HEAD"] and stripped:
        # assume that this is an S3 GET request with URL path `/<bucket>/<key ...>`
        return ServiceModelIdentifier("s3")

    # detect S3 URLs
    if stripped and "/" not in stripped:
        if method == "PUT":
            # assume that this is an S3 PUT bucket request with URL path `/<bucket>`
            return ServiceModelIdentifier("s3")
        if method == "POST" and "key" in request.values:
            # assume that this is an S3 POST request with form parameters or multipart form in the body
            return ServiceModelIdentifier("s3")

    # detect S3 requests sent from aws-cli using --no-sign-request option
    if "aws-cli/" in str(request.user_agent):
        return ServiceModelIdentifier("s3")

    # detect S3 pre-signed URLs (v2 and v4)
    values = request.values
    if any(
        value in values
        for value in [
            "AWSAccessKeyId",
            "Signature",
            "X-Amz-Algorithm",
            "X-Amz-Credential",
            "X-Amz-Date",
            "X-Amz-Expires",
            "X-Amz-SignedHeaders",
            "X-Amz-Signature",
        ]
    ):
        return ServiceModelIdentifier("s3")

    # S3 delete object requests
    if method == "POST" and "delete" in values:
        data_bytes = to_bytes(request.data)
        if b"<Delete" in data_bytes and b"<Key>" in data_bytes:
            return ServiceModelIdentifier("s3")

    # Put Object API can have multiple keys
    if stripped.count("/") >= 1 and method == "PUT":
        # assume that this is an S3 PUT bucket object request with URL path `/<bucket>/object`
        # or `/<bucket>/object/object1/+`
        return ServiceModelIdentifier("s3")

    # detect S3 requests with "AWS id:key" Auth headers
    auth_header = request.headers.get("Authorization") or ""
    if auth_header.startswith("AWS "):
        return ServiceModelIdentifier("s3")

    if uses_host_addressing(request.headers):
        # Note: This needs to be the last rule (and therefore is not in the host rules), since it is incredibly greedy
        return ServiceModelIdentifier("s3")


def resolve_conflicts(
    candidates: Set[ServiceModelIdentifier], request: Request
) -> ServiceModelIdentifier:
    """
    Some service definitions are overlapping to a point where they are _not_ distinguishable at all
    (f.e. ``DescribeEndpints`` in timestream-query and timestream-write).
    These conflicts need to be resolved manually.
    """
    service_name_candidates = {service.name for service in candidates}
    if service_name_candidates == {"timestream-query", "timestream-write"}:
        return ServiceModelIdentifier("timestream-query")
    if service_name_candidates == {"docdb", "neptune", "rds"}:
        return ServiceModelIdentifier("rds")
    if service_name_candidates == {"sqs"}:
        # SQS now have 2 different specs for `query` and `json` protocol. From our current implementation with the
        # parser and serializer, we need to have 2 different service names for them, but they share one provider
        # implementation. `sqs` represents the `json` protocol spec, and `sqs-query` the `query` protocol
        # (default again in botocore starting with 1.32.6).
        # The `application/x-amz-json-1.0` header is mandatory for requests targeting SQS with the `json` protocol. We
        # can safely route them to the `sqs` JSON parser/serializer. If not present, route the request to the
        # sqs-query protocol.
        content_type = request.headers.get("Content-Type")
        return (
            ServiceModelIdentifier("sqs")
            if content_type == "application/x-amz-json-1.0"
            else ServiceModelIdentifier("sqs", "query")
        )


def determine_aws_service_model_for_data_plane(
    request: Request, services: ServiceCatalog = None
) -> Optional[ServiceModel]:
    """
    A stripped down version of ``determine_aws_service_model`` which only checks hostname indicators for
    the AWS data plane, such as s3 websites, lambda function URLs, or API gateway routes.
    """
    custom_host_match = custom_host_addressing_rules(request.host)
    if custom_host_match:
        services = services or get_service_catalog()
        return services.get(*custom_host_match)


def determine_aws_service_model(
    request: Request, services: ServiceCatalog = None
) -> Optional[ServiceModel]:
    """
    Tries to determine the name of the AWS service an incoming request is targeting.
    :param request: to determine the target service name of
    :param services: service catalog (can be handed in for caching purposes)
    :return: service name string (or None if the targeting service could not be determined exactly)
    """
    services = services or get_service_catalog()
    signing_name, target_prefix, operation, host, path = _extract_service_indicators(request)
    candidates = set()

    # 1. check the signing names
    if signing_name:
        signing_name_candidates = services.by_signing_name(signing_name)
        if len(signing_name_candidates) == 1:
            # a unique signing-name -> service name mapping is the case for ~75% of service operations
            return services.get(*signing_name_candidates[0])

        # try to find a match with the custom signing name rules
        custom_match = custom_signing_name_rules(signing_name, path)
        if custom_match:
            return services.get(*custom_match)

        # still ambiguous - add the services to the list of candidates
        candidates.update(signing_name_candidates)

    # 2. check the target prefix
    if target_prefix and operation:
        target_candidates = services.by_target_prefix(target_prefix)
        if len(target_candidates) == 1:
            # a unique target prefix
            return services.get(*target_candidates[0])

        # still ambiguous - add the services to the list of candidates
        candidates.update(target_candidates)

        # exclude services where the operation is not contained in the service spec
        for service_identifier in list(candidates):
            service = services.get(*service_identifier)
            if operation not in service.operation_names:
                candidates.remove(service_identifier)
    else:
        # exclude services which have a target prefix (the current request does not have one)
        for service_identifier in list(candidates):
            service = services.get(*service_identifier)
            if service.metadata.get("targetPrefix") is not None:
                candidates.remove(service_identifier)

    if len(candidates) == 1:
        service_identifier = candidates.pop()
        return services.get(*service_identifier)

    # 3. check the path if it is set and not a trivial root path
    if path and path != "/":
        # try to find a match with the custom path rules
        custom_path_match = custom_path_addressing_rules(path)
        if custom_path_match:
            return services.get(*custom_path_match)

    # 4. check the host (custom host addressing rules)
    if host:
        # iterate over the service spec's endpoint prefix
        for prefix, services_per_prefix in services.endpoint_prefix_index.items():
            # this prevents a virtual host addressed bucket to be wrongly recognized
            if host.startswith(f"{prefix}.") and ".s3." not in host:
                if len(services_per_prefix) == 1:
                    return services.get(*services_per_prefix[0])
                candidates.update(services_per_prefix)

        custom_host_match = custom_host_addressing_rules(host)
        if custom_host_match:
            return services.get(*custom_host_match)

    if request.shallow:
        # from here on we would need access to the request body, which doesn't exist for shallow requests like
        # WebsocketRequests.
        return None

    # 5. check the query / form-data
    try:
        values = request.values
        if "Action" in values:
            # query / ec2 protocol requests always have an action and a version (the action is more significant)
            query_candidates = [
                service
                for service in services.by_operation(values["Action"])
                if service.protocol in ("ec2", "query")
            ]

            if len(query_candidates) == 1:
                return services.get(*query_candidates[0])

            if "Version" in values:
                for service_identifier in list(query_candidates):
                    service_model = services.get(*service_identifier)
                    if values["Version"] != service_model.api_version:
                        # the combination of Version and Action is not unique, add matches to the candidates
                        query_candidates.remove(service_identifier)

            if len(query_candidates) == 1:
                return services.get(*query_candidates[0])

            candidates.update(query_candidates)

    except RequestEntityTooLarge:
        # Some requests can be form-urlencoded but also contain binary data, which will fail the form parsing (S3 can
        # do this). In that case, skip this step and continue to try to determine the service name. The exception is
        # RequestEntityTooLarge even if the error is due to failed decoding.
        LOG.debug(
            "Failed to determine AWS service from request body because the form could not be parsed",
            exc_info=LOG.isEnabledFor(logging.DEBUG),
        )

    # 6. resolve service spec conflicts
    resolved_conflict = resolve_conflicts(candidates, request)
    if resolved_conflict:
        return services.get(*resolved_conflict)

    # 7. check the legacy S3 rules in the end
    legacy_match = legacy_s3_rules(request)
    if legacy_match:
        return services.get(*legacy_match)

    if signing_name:
        return services.get(name=signing_name)
    if candidates:
        return services.get(*candidates.pop())
    return None
