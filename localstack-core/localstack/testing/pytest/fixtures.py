import contextlib
import dataclasses
import json
import logging
import os
import re
import textwrap
import time
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Tuple, Unpack

import botocore.auth
import botocore.config
import botocore.credentials
import botocore.session
import pytest
from _pytest.config import Config
from _pytest.nodes import Item
from botocore.exceptions import ClientError
from botocore.regions import EndpointResolver
from pytest_httpserver import HTTPServer
from werkzeug import Request, Response

from localstack import config
from localstack.aws.api.ec2 import CreateSecurityGroupRequest, CreateVpcEndpointRequest, VpcEndpoint
from localstack.aws.connect import ServiceLevelClientFactory
from localstack.services.stores import (
    AccountRegionBundle,
    BaseStore,
    CrossAccountAttribute,
    CrossRegionAttribute,
    LocalAttribute,
)
from localstack.testing.aws.cloudformation_utils import load_template_file, render_template
from localstack.testing.aws.util import get_lambda_logs, is_aws_cloud
from localstack.testing.config import (
    SECONDARY_TEST_AWS_ACCOUNT_ID,
    SECONDARY_TEST_AWS_REGION_NAME,
    TEST_AWS_ACCOUNT_ID,
    TEST_AWS_REGION_NAME,
)
from localstack.utils import testutil
from localstack.utils.aws.arns import get_partition
from localstack.utils.aws.client import SigningHttpClient
from localstack.utils.aws.resources import create_dynamodb_table
from localstack.utils.bootstrap import is_api_enabled
from localstack.utils.collections import ensure_list, select_from_typed_dict
from localstack.utils.functions import call_safe, run_safe
from localstack.utils.http import safe_requests as requests
from localstack.utils.id_generator import ResourceIdentifier, localstack_id_manager
from localstack.utils.json import CustomEncoder, json_safe
from localstack.utils.net import wait_for_port_open
from localstack.utils.strings import short_uid, to_str
from localstack.utils.sync import ShortCircuitWaitException, poll_condition, retry, wait_until

LOG = logging.getLogger(__name__)

# URL of public HTTP echo server, used primarily for AWS parity/snapshot testing
PUBLIC_HTTP_ECHO_SERVER_URL = "http://httpbin.org"

WAITER_CHANGE_SET_CREATE_COMPLETE = "change_set_create_complete"
WAITER_STACK_CREATE_COMPLETE = "stack_create_complete"
WAITER_STACK_UPDATE_COMPLETE = "stack_update_complete"
WAITER_STACK_DELETE_COMPLETE = "stack_delete_complete"


if TYPE_CHECKING:
    from mypy_boto3_sqs import SQSClient
    from mypy_boto3_sqs.type_defs import MessageTypeDef


@pytest.fixture(scope="session")
def aws_client_no_retry(aws_client_factory):
    """
    This fixture can be used to obtain Boto clients with disabled retries for testing.
    botocore docs: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/retries.html#configuring-a-retry-mode

    Use this client when testing exceptions (i.e., with pytest.raises(...)) or expected errors (e.g., status code 500)
    to avoid unnecessary retries and mitigate test flakiness if the tested error condition is time-bound.

    This client is needed for the following errors, exceptions, and HTTP status codes defined by the legacy retry mode:
    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/retries.html#legacy-retry-mode
    General socket/connection errors:
    * ConnectionError
    * ConnectionClosedError
    * ReadTimeoutError
    * EndpointConnectionError

    Service-side throttling/limit errors and exceptions:
    * Throttling
    * ThrottlingException
    * ThrottledException
    * RequestThrottledException
    * ProvisionedThroughputExceededException

    HTTP status codes: 429, 500, 502, 503, 504, and 509

    Hence, this client is not needed for a `ResourceNotFound` error (but it doesn't harm).
    """
    no_retry_config = botocore.config.Config(retries={"max_attempts": 1})
    return aws_client_factory(config=no_retry_config)


@pytest.fixture(scope="class")
def aws_http_client_factory(aws_session):
    """
    Returns a factory for creating new ``SigningHttpClient`` instances using a configurable botocore request signer.
    The default signer is a SigV4QueryAuth. The credentials are extracted from the ``boto3_sessions`` fixture that
    transparently uses your global profile when TEST_TARGET=AWS_CLOUD, or test credentials when running against
    LocalStack.

    Example invocations

        client = aws_signing_http_client_factory("sqs")
        client.get("http://localhost:4566/000000000000/my-queue")

    or
        client = aws_signing_http_client_factory("dynamodb", signer_factory=SigV4Auth)
        client.post("...")
    """

    def factory(
        service: str,
        region: str = None,
        signer_factory: Callable[
            [botocore.credentials.Credentials, str, str], botocore.auth.BaseSigner
        ] = botocore.auth.SigV4QueryAuth,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
    ):
        region = region or TEST_AWS_REGION_NAME

        if aws_access_key_id or aws_secret_access_key:
            credentials = botocore.credentials.Credentials(
                access_key=aws_access_key_id, secret_key=aws_secret_access_key
            )
        else:
            credentials = aws_session.get_credentials()

        creds = credentials.get_frozen_credentials()

        if not endpoint_url:
            if is_aws_cloud():
                # FIXME: this is a bit raw. we should probably re-use boto in a better way
                resolver: EndpointResolver = aws_session._session.get_component("endpoint_resolver")
                endpoint_url = "https://" + resolver.construct_endpoint(service, region)["hostname"]
            else:
                endpoint_url = config.internal_service_url()

        return SigningHttpClient(signer_factory(creds, service, region), endpoint_url=endpoint_url)

    return factory


@pytest.fixture(scope="class")
def s3_vhost_client(aws_client_factory, region_name):
    return aws_client_factory(
        config=botocore.config.Config(s3={"addressing_style": "virtual"}), region_name=region_name
    ).s3


@pytest.fixture
def dynamodb_wait_for_table_active(aws_client):
    def wait_for_table_active(table_name: str, client=None):
        def wait():
            return (client or aws_client.dynamodb).describe_table(TableName=table_name)["Table"][
                "TableStatus"
            ] == "ACTIVE"

        poll_condition(wait, timeout=30)

    return wait_for_table_active


@pytest.fixture
def dynamodb_create_table_with_parameters(dynamodb_wait_for_table_active, aws_client):
    tables = []

    def factory(**kwargs):
        if "TableName" not in kwargs:
            kwargs["TableName"] = f"test-table-{short_uid()}"

        tables.append(kwargs["TableName"])
        response = aws_client.dynamodb.create_table(**kwargs)
        dynamodb_wait_for_table_active(kwargs["TableName"])
        return response

    yield factory

    # cleanup
    for table in tables:
        try:
            # table has to be in ACTIVE state before deletion
            dynamodb_wait_for_table_active(table)
            aws_client.dynamodb.delete_table(TableName=table)
        except Exception as e:
            LOG.debug("error cleaning up table %s: %s", table, e)


@pytest.fixture
def dynamodb_create_table(dynamodb_wait_for_table_active, aws_client):
    # beware, this swallows exception in create_dynamodb_table utility function
    tables = []

    def factory(**kwargs):
        kwargs["client"] = aws_client.dynamodb
        if "table_name" not in kwargs:
            kwargs["table_name"] = f"test-table-{short_uid()}"
        if "partition_key" not in kwargs:
            kwargs["partition_key"] = "id"

        tables.append(kwargs["table_name"])

        return create_dynamodb_table(**kwargs)

    yield factory

    # cleanup
    for table in tables:
        try:
            # table has to be in ACTIVE state before deletion
            dynamodb_wait_for_table_active(table)
            aws_client.dynamodb.delete_table(TableName=table)
        except Exception as e:
            LOG.debug("error cleaning up table %s: %s", table, e)


@pytest.fixture
def s3_create_bucket(s3_empty_bucket, aws_client):
    buckets = []

    def factory(**kwargs) -> str:
        if "Bucket" not in kwargs:
            kwargs["Bucket"] = "test-bucket-%s" % short_uid()

        if (
            "CreateBucketConfiguration" not in kwargs
            and aws_client.s3.meta.region_name != "us-east-1"
        ):
            kwargs["CreateBucketConfiguration"] = {
                "LocationConstraint": aws_client.s3.meta.region_name
            }

        aws_client.s3.create_bucket(**kwargs)
        buckets.append(kwargs["Bucket"])
        return kwargs["Bucket"]

    yield factory

    # cleanup
    for bucket in buckets:
        try:
            s3_empty_bucket(bucket)
            aws_client.s3.delete_bucket(Bucket=bucket)
        except Exception as e:
            LOG.debug("error cleaning up bucket %s: %s", bucket, e)


@pytest.fixture
def s3_create_bucket_with_client(s3_empty_bucket, aws_client):
    buckets = []

    def factory(s3_client, **kwargs) -> str:
        if "Bucket" not in kwargs:
            kwargs["Bucket"] = f"test-bucket-{short_uid()}"

        response = s3_client.create_bucket(**kwargs)
        buckets.append(kwargs["Bucket"])
        return response

    yield factory

    # cleanup
    for bucket in buckets:
        try:
            s3_empty_bucket(bucket)
            aws_client.s3.delete_bucket(Bucket=bucket)
        except Exception as e:
            LOG.debug("error cleaning up bucket %s: %s", bucket, e)


@pytest.fixture
def s3_bucket(s3_create_bucket, aws_client) -> str:
    region = aws_client.s3.meta.region_name
    kwargs = {}
    if region != "us-east-1":
        kwargs["CreateBucketConfiguration"] = {"LocationConstraint": region}
    return s3_create_bucket(**kwargs)


@pytest.fixture
def s3_empty_bucket(aws_client):
    """
    Returns a factory that given a bucket name, deletes all objects and deletes all object versions
    """

    # Boto resource would make this a straightforward task, but our internal client does not support Boto resource
    # FIXME: this won't work when bucket has more than 1000 objects
    def factory(bucket_name: str):
        kwargs = {}
        try:
            aws_client.s3.get_object_lock_configuration(Bucket=bucket_name)
            kwargs["BypassGovernanceRetention"] = True
        except ClientError:
            pass

        response = aws_client.s3.list_objects_v2(Bucket=bucket_name)
        objects = [{"Key": obj["Key"]} for obj in response.get("Contents", [])]
        if objects:
            aws_client.s3.delete_objects(
                Bucket=bucket_name,
                Delete={"Objects": objects},
                **kwargs,
            )

        response = aws_client.s3.list_object_versions(Bucket=bucket_name)
        versions = response.get("Versions", [])
        versions.extend(response.get("DeleteMarkers", []))

        object_versions = [{"Key": obj["Key"], "VersionId": obj["VersionId"]} for obj in versions]
        if object_versions:
            aws_client.s3.delete_objects(
                Bucket=bucket_name,
                Delete={"Objects": object_versions},
                **kwargs,
            )

    yield factory


@pytest.fixture
def sqs_create_queue(aws_client):
    queue_urls = []

    def factory(**kwargs):
        if "QueueName" not in kwargs:
            kwargs["QueueName"] = "test-queue-%s" % short_uid()

        response = aws_client.sqs.create_queue(**kwargs)
        url = response["QueueUrl"]
        queue_urls.append(url)

        return url

    yield factory

    # cleanup
    for queue_url in queue_urls:
        try:
            aws_client.sqs.delete_queue(QueueUrl=queue_url)
        except Exception as e:
            LOG.debug("error cleaning up queue %s: %s", queue_url, e)


@pytest.fixture
def sqs_receive_messages_delete(aws_client):
    def factory(
        queue_url: str,
        expected_messages: Optional[int] = None,
        wait_time: Optional[int] = 5,
    ):
        response = aws_client.sqs.receive_message(
            QueueUrl=queue_url,
            MessageAttributeNames=["All"],
            VisibilityTimeout=0,
            WaitTimeSeconds=wait_time,
        )
        messages = []
        for m in response["Messages"]:
            message = json.loads(to_str(m["Body"]))
            messages.append(message)

        if expected_messages is not None:
            assert len(messages) == expected_messages

        for message in response["Messages"]:
            aws_client.sqs.delete_message(
                QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"]
            )

        return messages

    return factory


@pytest.fixture
def sqs_receive_num_messages(sqs_receive_messages_delete):
    def factory(queue_url: str, expected_messages: int, max_iterations: int = 3):
        all_messages = []
        for _ in range(max_iterations):
            try:
                messages = sqs_receive_messages_delete(queue_url, wait_time=5)
            except KeyError:
                # there were no messages
                continue
            all_messages.extend(messages)

            if len(all_messages) >= expected_messages:
                return all_messages[:expected_messages]

        raise AssertionError(f"max iterations reached with {len(all_messages)} messages received")

    return factory


@pytest.fixture
def sqs_collect_messages(aws_client):
    """Collects SQS messages from a given queue_url and deletes them by default.
    Example usage:
    messages = sqs_collect_messages(
         my_queue_url,
         expected=2,
         timeout=10,
         attribute_names=["All"],
         message_attribute_names=["All"],
    )
    """

    def factory(
        queue_url: str,
        expected: int,
        timeout: int,
        delete: bool = True,
        attribute_names: list[str] = None,
        message_attribute_names: list[str] = None,
        max_number_of_messages: int = 1,
        wait_time_seconds: int = 5,
        sqs_client: "SQSClient | None" = None,
    ) -> list["MessageTypeDef"]:
        sqs_client = sqs_client or aws_client.sqs
        collected = []

        def _receive():
            response = sqs_client.receive_message(
                QueueUrl=queue_url,
                # Maximum is 20 seconds. Performs long polling.
                WaitTimeSeconds=wait_time_seconds,
                # Maximum 10 messages
                MaxNumberOfMessages=max_number_of_messages,
                AttributeNames=attribute_names or [],
                MessageAttributeNames=message_attribute_names or [],
            )

            if messages := response.get("Messages"):
                collected.extend(messages)

                if delete:
                    for m in messages:
                        sqs_client.delete_message(
                            QueueUrl=queue_url, ReceiptHandle=m["ReceiptHandle"]
                        )

            return len(collected) >= expected

        if not poll_condition(_receive, timeout=timeout):
            raise TimeoutError(
                f"gave up waiting for messages (expected={expected}, actual={len(collected)}"
            )

        return collected

    yield factory


@pytest.fixture
def sqs_queue(sqs_create_queue):
    return sqs_create_queue()


@pytest.fixture
def sqs_get_queue_arn(aws_client) -> Callable:
    def _get_queue_arn(queue_url: str) -> str:
        return aws_client.sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=["QueueArn"])[
            "Attributes"
        ]["QueueArn"]

    return _get_queue_arn


@pytest.fixture
def sqs_queue_exists(aws_client):
    def _queue_exists(queue_url: str) -> bool:
        """
        Checks whether a queue with the given queue URL exists.
        :param queue_url: the queue URL
        :return: true if the queue exists, false otherwise
        """
        try:
            result = aws_client.sqs.get_queue_url(QueueName=queue_url.split("/")[-1])
            return result.get("QueueUrl") == queue_url
        except ClientError as e:
            if "NonExistentQueue" in e.response["Error"]["Code"]:
                return False
            raise

    yield _queue_exists


@pytest.fixture
def sns_create_topic(aws_client):
    topic_arns = []

    def _create_topic(**kwargs):
        if "Name" not in kwargs:
            kwargs["Name"] = "test-topic-%s" % short_uid()
        response = aws_client.sns.create_topic(**kwargs)
        topic_arns.append(response["TopicArn"])
        return response

    yield _create_topic

    for topic_arn in topic_arns:
        try:
            aws_client.sns.delete_topic(TopicArn=topic_arn)
        except Exception as e:
            LOG.debug("error cleaning up topic %s: %s", topic_arn, e)


@pytest.fixture
def sns_wait_for_topic_delete(aws_client):
    def wait_for_topic_delete(topic_arn: str) -> None:
        def wait():
            try:
                aws_client.sns.get_topic_attributes(TopicArn=topic_arn)
                return False
            except Exception as e:
                if "NotFound" in e.response["Error"]["Code"]:
                    return True

                raise

        poll_condition(wait, timeout=30)

    return wait_for_topic_delete


@pytest.fixture
def sns_subscription(aws_client):
    sub_arns = []

    def _create_sub(**kwargs):
        if kwargs.get("ReturnSubscriptionArn") is None:
            kwargs["ReturnSubscriptionArn"] = True

        # requires 'TopicArn', 'Protocol', and 'Endpoint'
        response = aws_client.sns.subscribe(**kwargs)
        sub_arn = response["SubscriptionArn"]
        sub_arns.append(sub_arn)
        return response

    yield _create_sub

    for sub_arn in sub_arns:
        try:
            aws_client.sns.unsubscribe(SubscriptionArn=sub_arn)
        except Exception as e:
            LOG.debug("error cleaning up subscription %s: %s", sub_arn, e)


@pytest.fixture
def sns_topic(sns_create_topic, aws_client):
    topic_arn = sns_create_topic()["TopicArn"]
    return aws_client.sns.get_topic_attributes(TopicArn=topic_arn)


@pytest.fixture
def sns_allow_topic_sqs_queue(aws_client):
    def _allow_sns_topic(sqs_queue_url, sqs_queue_arn, sns_topic_arn) -> None:
        # allow topic to write to sqs queue
        aws_client.sqs.set_queue_attributes(
            QueueUrl=sqs_queue_url,
            Attributes={
                "Policy": json.dumps(
                    {
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Principal": {"Service": "sns.amazonaws.com"},
                                "Action": "sqs:SendMessage",
                                "Resource": sqs_queue_arn,
                                "Condition": {"ArnEquals": {"aws:SourceArn": sns_topic_arn}},
                            }
                        ]
                    }
                )
            },
        )

    return _allow_sns_topic


@pytest.fixture
def sns_create_sqs_subscription(sns_allow_topic_sqs_queue, sqs_get_queue_arn, aws_client):
    subscriptions = []

    def _factory(topic_arn: str, queue_url: str, **kwargs) -> Dict[str, str]:
        queue_arn = sqs_get_queue_arn(queue_url)

        # connect sns topic to sqs
        subscription = aws_client.sns.subscribe(
            TopicArn=topic_arn, Protocol="sqs", Endpoint=queue_arn, **kwargs
        )
        subscription_arn = subscription["SubscriptionArn"]

        # allow topic to write to sqs queue
        sns_allow_topic_sqs_queue(
            sqs_queue_url=queue_url, sqs_queue_arn=queue_arn, sns_topic_arn=topic_arn
        )

        subscriptions.append(subscription_arn)
        return aws_client.sns.get_subscription_attributes(SubscriptionArn=subscription_arn)[
            "Attributes"
        ]

    yield _factory

    for arn in subscriptions:
        try:
            aws_client.sns.unsubscribe(SubscriptionArn=arn)
        except Exception as e:
            LOG.error("error cleaning up subscription %s: %s", arn, e)


@pytest.fixture
def sns_create_http_endpoint(sns_create_topic, sns_subscription, aws_client):
    # This fixture can be used with manual setup to expose the HTTPServer fixture to AWS. One example is to use a
    # a service like localhost.run, and set up a specific port to start the `HTTPServer(port=40000)` for example,
    # and tunnel `localhost:40000` to a specific domain that you can manually return from this fixture.
    http_servers = []

    def _create_http_endpoint(
        raw_message_delivery: bool = False,
    ) -> Tuple[str, str, str, HTTPServer]:
        server = HTTPServer()
        server.start()
        http_servers.append(server)
        server.expect_request("/sns-endpoint").respond_with_data(status=200)
        endpoint_url = server.url_for("/sns-endpoint")
        wait_for_port_open(endpoint_url)

        topic_arn = sns_create_topic()["TopicArn"]
        subscription = sns_subscription(TopicArn=topic_arn, Protocol="http", Endpoint=endpoint_url)
        subscription_arn = subscription["SubscriptionArn"]
        delivery_policy = {
            "healthyRetryPolicy": {
                "minDelayTarget": 1,
                "maxDelayTarget": 1,
                "numRetries": 0,
                "numNoDelayRetries": 0,
                "numMinDelayRetries": 0,
                "numMaxDelayRetries": 0,
                "backoffFunction": "linear",
            },
            "sicklyRetryPolicy": None,
            "throttlePolicy": {"maxReceivesPerSecond": 1000},
            "guaranteed": False,
        }
        aws_client.sns.set_subscription_attributes(
            SubscriptionArn=subscription_arn,
            AttributeName="DeliveryPolicy",
            AttributeValue=json.dumps(delivery_policy),
        )

        if raw_message_delivery:
            aws_client.sns.set_subscription_attributes(
                SubscriptionArn=subscription_arn,
                AttributeName="RawMessageDelivery",
                AttributeValue="true",
            )

        return topic_arn, subscription_arn, endpoint_url, server

    yield _create_http_endpoint

    for http_server in http_servers:
        if http_server.is_running():
            http_server.stop()


@pytest.fixture
def route53_hosted_zone(aws_client):
    hosted_zones = []

    def factory(**kwargs):
        if "Name" not in kwargs:
            kwargs["Name"] = f"www.{short_uid()}.com."
        if "CallerReference" not in kwargs:
            kwargs["CallerReference"] = f"caller-ref-{short_uid()}"
        response = aws_client.route53.create_hosted_zone(
            Name=kwargs["Name"], CallerReference=kwargs["CallerReference"]
        )
        hosted_zones.append(response["HostedZone"]["Id"])
        return response

    yield factory

    for zone in hosted_zones:
        try:
            aws_client.route53.delete_hosted_zone(Id=zone)
        except Exception as e:
            LOG.debug("error cleaning up route53 HostedZone %s: %s", zone, e)


@pytest.fixture
def transcribe_create_job(s3_bucket, aws_client):
    job_names = []

    def _create_job(audio_file: str, params: Optional[dict[str, Any]] = None) -> str:
        s3_key = "test-clip.wav"

        if not params:
            params = {}

        if "TranscriptionJobName" not in params:
            params["TranscriptionJobName"] = f"test-transcribe-{short_uid()}"

        if "LanguageCode" not in params:
            params["LanguageCode"] = "en-GB"

        if "Media" not in params:
            params["Media"] = {"MediaFileUri": f"s3://{s3_bucket}/{s3_key}"}

        # upload test wav to a s3 bucket
        with open(audio_file, "rb") as f:
            aws_client.s3.upload_fileobj(f, s3_bucket, s3_key)

        response = aws_client.transcribe.start_transcription_job(**params)

        job_name = response["TranscriptionJob"]["TranscriptionJobName"]
        job_names.append(job_name)

        return job_name

    yield _create_job

    for job_name in job_names:
        with contextlib.suppress(ClientError):
            aws_client.transcribe.delete_transcription_job(TranscriptionJobName=job_name)


@pytest.fixture
def kinesis_create_stream(aws_client):
    stream_names = []

    def _create_stream(**kwargs):
        if "StreamName" not in kwargs:
            kwargs["StreamName"] = f"test-stream-{short_uid()}"
        aws_client.kinesis.create_stream(**kwargs)
        stream_names.append(kwargs["StreamName"])
        return kwargs["StreamName"]

    yield _create_stream

    for stream_name in stream_names:
        try:
            aws_client.kinesis.delete_stream(StreamName=stream_name, EnforceConsumerDeletion=True)
        except Exception as e:
            LOG.debug("error cleaning up kinesis stream %s: %s", stream_name, e)


@pytest.fixture
def wait_for_stream_ready(aws_client):
    def _wait_for_stream_ready(stream_name: str):
        def is_stream_ready():
            describe_stream_response = aws_client.kinesis.describe_stream(StreamName=stream_name)
            return describe_stream_response["StreamDescription"]["StreamStatus"] in [
                "ACTIVE",
                "UPDATING",
            ]

        return poll_condition(is_stream_ready)

    return _wait_for_stream_ready


@pytest.fixture
def wait_for_delivery_stream_ready(aws_client):
    def _wait_for_stream_ready(delivery_stream_name: str):
        def is_stream_ready():
            describe_stream_response = aws_client.firehose.describe_delivery_stream(
                DeliveryStreamName=delivery_stream_name
            )
            return (
                describe_stream_response["DeliveryStreamDescription"]["DeliveryStreamStatus"]
                == "ACTIVE"
            )

        poll_condition(is_stream_ready)

    return _wait_for_stream_ready


@pytest.fixture
def wait_for_dynamodb_stream_ready(aws_client):
    def _wait_for_stream_ready(stream_arn: str, client=None):
        def is_stream_ready():
            ddb_client = client or aws_client.dynamodbstreams
            describe_stream_response = ddb_client.describe_stream(StreamArn=stream_arn)
            return describe_stream_response["StreamDescription"]["StreamStatus"] == "ENABLED"

        return poll_condition(is_stream_ready)

    return _wait_for_stream_ready


@pytest.fixture()
def kms_create_key(aws_client_factory):
    key_ids = []

    def _create_key(region_name: str = None, **kwargs):
        if "Description" not in kwargs:
            kwargs["Description"] = f"test description - {short_uid()}"
        key_metadata = aws_client_factory(region_name=region_name).kms.create_key(**kwargs)[
            "KeyMetadata"
        ]
        key_ids.append((region_name, key_metadata["KeyId"]))
        return key_metadata

    yield _create_key

    for region_name, key_id in key_ids:
        try:
            # shortest amount of time you can schedule the deletion
            aws_client_factory(region_name=region_name).kms.schedule_key_deletion(
                KeyId=key_id, PendingWindowInDays=7
            )
        except Exception as e:
            exception_message = str(e)
            # Some tests schedule their keys for deletion themselves.
            if (
                "KMSInvalidStateException" not in exception_message
                or "is pending deletion" not in exception_message
            ):
                LOG.debug("error cleaning up KMS key %s: %s", key_id, e)


@pytest.fixture()
def kms_replicate_key(aws_client_factory):
    key_ids = []

    def _replicate_key(region_from=None, **kwargs):
        region_to = kwargs.get("ReplicaRegion")
        key_ids.append((region_to, kwargs.get("KeyId")))
        return aws_client_factory(region_name=region_from).kms.replicate_key(**kwargs)

    yield _replicate_key

    for region_to, key_id in key_ids:
        try:
            # shortest amount of time you can schedule the deletion
            aws_client_factory(region_name=region_to).kms.schedule_key_deletion(
                KeyId=key_id, PendingWindowInDays=7
            )
        except Exception as e:
            LOG.debug("error cleaning up KMS key %s: %s", key_id, e)


# kms_create_key fixture is used here not just to be able to create aliases without a key specified,
# but also to make sure that kms_create_key gets executed before and teared down after kms_create_alias -
# to make sure that we clean up aliases before keys get cleaned up.
@pytest.fixture()
def kms_create_alias(kms_create_key, aws_client):
    aliases = []

    def _create_alias(**kwargs):
        if "AliasName" not in kwargs:
            kwargs["AliasName"] = f"alias/{short_uid()}"
        if "TargetKeyId" not in kwargs:
            kwargs["TargetKeyId"] = kms_create_key()["KeyId"]

        aws_client.kms.create_alias(**kwargs)
        aliases.append(kwargs["AliasName"])
        return kwargs["AliasName"]

    yield _create_alias

    for alias in aliases:
        try:
            aws_client.kms.delete_alias(AliasName=alias)
        except Exception as e:
            LOG.debug("error cleaning up KMS alias %s: %s", alias, e)


@pytest.fixture()
def kms_create_grant(kms_create_key, aws_client):
    grants = []

    def _create_grant(**kwargs):
        # Just a random ARN, since KMS in LocalStack currently doesn't validate GranteePrincipal,
        # but some GranteePrincipal is required to create a grant.
        GRANTEE_PRINCIPAL_ARN = (
            "arn:aws:kms:eu-central-1:123456789876:key/198a5a78-52c3-489f-ac70-b06a4d11027a"
        )

        if "Operations" not in kwargs:
            kwargs["Operations"] = ["Decrypt", "Encrypt"]
        if "GranteePrincipal" not in kwargs:
            kwargs["GranteePrincipal"] = GRANTEE_PRINCIPAL_ARN
        if "KeyId" not in kwargs:
            kwargs["KeyId"] = kms_create_key()["KeyId"]

        grant_id = aws_client.kms.create_grant(**kwargs)["GrantId"]
        grants.append((grant_id, kwargs["KeyId"]))
        return grant_id, kwargs["KeyId"]

    yield _create_grant

    for grant_id, key_id in grants:
        try:
            aws_client.kms.retire_grant(GrantId=grant_id, KeyId=key_id)
        except Exception as e:
            LOG.debug("error cleaning up KMS grant %s: %s", grant_id, e)


@pytest.fixture
def kms_key(kms_create_key):
    return kms_create_key()


@pytest.fixture
def kms_grant_and_key(kms_key, aws_client):
    user_arn = aws_client.sts.get_caller_identity()["Arn"]

    return [
        aws_client.kms.create_grant(
            KeyId=kms_key["KeyId"],
            GranteePrincipal=user_arn,
            Operations=["Decrypt", "Encrypt"],
        ),
        kms_key,
    ]


@pytest.fixture
def opensearch_wait_for_cluster(aws_client):
    def _wait_for_cluster(domain_name: str):
        def finished_processing():
            status = aws_client.opensearch.describe_domain(DomainName=domain_name)["DomainStatus"]
            return status["DomainProcessingStatus"] == "Active" and "Endpoint" in status

        assert poll_condition(
            finished_processing, timeout=25 * 60, **({"interval": 10} if is_aws_cloud() else {})
        ), f"could not start domain: {domain_name}"

    return _wait_for_cluster


@pytest.fixture
def opensearch_create_domain(opensearch_wait_for_cluster, aws_client):
    domains = []

    def factory(**kwargs) -> str:
        if "DomainName" not in kwargs:
            kwargs["DomainName"] = f"test-domain-{short_uid()}"

        aws_client.opensearch.create_domain(**kwargs)

        opensearch_wait_for_cluster(domain_name=kwargs["DomainName"])

        domains.append(kwargs["DomainName"])
        return kwargs["DomainName"]

    yield factory

    # cleanup
    for domain in domains:
        try:
            aws_client.opensearch.delete_domain(DomainName=domain)
        except Exception as e:
            LOG.debug("error cleaning up domain %s: %s", domain, e)


@pytest.fixture
def opensearch_domain(opensearch_create_domain) -> str:
    return opensearch_create_domain()


@pytest.fixture
def opensearch_endpoint(opensearch_domain, aws_client) -> str:
    status = aws_client.opensearch.describe_domain(DomainName=opensearch_domain)["DomainStatus"]
    assert "Endpoint" in status
    return f"https://{status['Endpoint']}"


@pytest.fixture
def opensearch_document_path(opensearch_endpoint, aws_client):
    document = {
        "first_name": "Boba",
        "last_name": "Fett",
        "age": 41,
        "about": "I'm just a simple man, trying to make my way in the universe.",
        "interests": ["mandalorian armor", "tusken culture"],
    }
    document_path = f"{opensearch_endpoint}/bountyhunters/_doc/1"
    response = requests.put(
        document_path,
        data=json.dumps(document),
        headers={"content-type": "application/json", "Accept-encoding": "identity"},
    )
    assert response.status_code == 201, f"could not create document at: {document_path}"
    return document_path


# Cleanup fixtures
@pytest.fixture
def cleanup_stacks(aws_client):
    def _cleanup_stacks(stacks: List[str]) -> None:
        stacks = ensure_list(stacks)
        for stack in stacks:
            try:
                aws_client.cloudformation.delete_stack(StackName=stack)
                aws_client.cloudformation.get_waiter("stack_delete_complete").wait(StackName=stack)
            except Exception:
                LOG.debug("Failed to cleanup stack '%s'", stack)

    return _cleanup_stacks


@pytest.fixture
def cleanup_changesets(aws_client):
    def _cleanup_changesets(changesets: List[str]) -> None:
        changesets = ensure_list(changesets)
        for cs in changesets:
            try:
                aws_client.cloudformation.delete_change_set(ChangeSetName=cs)
            except Exception:
                LOG.debug("Failed to cleanup changeset '%s'", cs)

    return _cleanup_changesets


# Helpers for Cfn


# TODO: exports(!)
@dataclasses.dataclass(frozen=True)
class DeployResult:
    change_set_id: str
    stack_id: str
    stack_name: str
    change_set_name: str
    outputs: Dict[str, str]

    destroy: Callable[[], None]


class StackDeployError(Exception):
    def __init__(self, describe_res: dict, events: list[dict]):
        self.describe_result = describe_res
        self.events = events

        encoded_describe_output = json.dumps(self.describe_result, cls=CustomEncoder)
        if config.CFN_VERBOSE_ERRORS:
            msg = f"Describe output:\n{encoded_describe_output}\nEvents:\n{self.format_events(events)}"
        else:
            msg = f"Describe output:\n{encoded_describe_output}\nFailing resources:\n{self.format_events(events)}"

        super().__init__(msg)

    def format_events(self, events: list[dict]) -> str:
        formatted_events = []

        chronological_events = sorted(events, key=lambda event: event["Timestamp"])
        for event in chronological_events:
            if event["ResourceStatus"].endswith("FAILED") or config.CFN_VERBOSE_ERRORS:
                formatted_events.append(self.format_event(event))

        return "\n".join(formatted_events)

    @staticmethod
    def format_event(event: dict) -> str:
        if reason := event.get("ResourceStatusReason"):
            reason = reason.replace("\n", "; ")
            return f"- {event['LogicalResourceId']} ({event['ResourceType']}) -> {event['ResourceStatus']} ({reason})"
        else:
            return f"- {event['LogicalResourceId']} ({event['ResourceType']}) -> {event['ResourceStatus']}"


@pytest.fixture
def deploy_cfn_template(
    aws_client: ServiceLevelClientFactory,
):
    state: list[tuple[str, Callable]] = []

    def _deploy(
        *,
        is_update: Optional[bool] = False,
        stack_name: Optional[str] = None,
        change_set_name: Optional[str] = None,
        template: Optional[str] = None,
        template_path: Optional[str | os.PathLike] = None,
        template_mapping: Optional[Dict[str, Any]] = None,
        parameters: Optional[Dict[str, str]] = None,
        role_arn: Optional[str] = None,
        max_wait: Optional[int] = None,
        delay_between_polls: Optional[int] = 2,
        custom_aws_client: Optional[ServiceLevelClientFactory] = None,
    ) -> DeployResult:
        if is_update:
            assert stack_name
        stack_name = stack_name or f"stack-{short_uid()}"
        change_set_name = change_set_name or f"change-set-{short_uid()}"

        if max_wait is None:
            max_wait = 1800 if is_aws_cloud() else 180

        if template_path is not None:
            template = load_template_file(template_path)
            if template is None:
                raise RuntimeError(f"Could not find file {os.path.realpath(template_path)}")
        template_rendered = render_template(template, **(template_mapping or {}))

        kwargs = dict(
            StackName=stack_name,
            ChangeSetName=change_set_name,
            TemplateBody=template_rendered,
            Capabilities=["CAPABILITY_AUTO_EXPAND", "CAPABILITY_IAM", "CAPABILITY_NAMED_IAM"],
            ChangeSetType=("UPDATE" if is_update else "CREATE"),
            Parameters=[
                {
                    "ParameterKey": k,
                    "ParameterValue": v,
                }
                for (k, v) in (parameters or {}).items()
            ],
        )
        if role_arn is not None:
            kwargs["RoleARN"] = role_arn

        cfn_aws_client = custom_aws_client if custom_aws_client is not None else aws_client

        response = cfn_aws_client.cloudformation.create_change_set(**kwargs)

        change_set_id = response["Id"]
        stack_id = response["StackId"]

        cfn_aws_client.cloudformation.get_waiter(WAITER_CHANGE_SET_CREATE_COMPLETE).wait(
            ChangeSetName=change_set_id
        )
        cfn_aws_client.cloudformation.execute_change_set(ChangeSetName=change_set_id)
        stack_waiter = cfn_aws_client.cloudformation.get_waiter(
            WAITER_STACK_UPDATE_COMPLETE if is_update else WAITER_STACK_CREATE_COMPLETE
        )

        try:
            stack_waiter.wait(
                StackName=stack_id,
                WaiterConfig={
                    "Delay": delay_between_polls,
                    "MaxAttempts": max_wait / delay_between_polls,
                },
            )
        except botocore.exceptions.WaiterError as e:
            raise StackDeployError(
                cfn_aws_client.cloudformation.describe_stacks(StackName=stack_id)["Stacks"][0],
                cfn_aws_client.cloudformation.describe_stack_events(StackName=stack_id)[
                    "StackEvents"
                ],
            ) from e

        describe_stack_res = cfn_aws_client.cloudformation.describe_stacks(StackName=stack_id)[
            "Stacks"
        ][0]
        outputs = describe_stack_res.get("Outputs", [])

        mapped_outputs = {o["OutputKey"]: o.get("OutputValue") for o in outputs}

        def _destroy_stack():
            cfn_aws_client.cloudformation.delete_stack(StackName=stack_id)
            cfn_aws_client.cloudformation.get_waiter(WAITER_STACK_DELETE_COMPLETE).wait(
                StackName=stack_id,
                WaiterConfig={
                    "Delay": delay_between_polls,
                    "MaxAttempts": max_wait / delay_between_polls,
                },
            )

        state.append((stack_id, _destroy_stack))

        return DeployResult(
            change_set_id, stack_id, stack_name, change_set_name, mapped_outputs, _destroy_stack
        )

    yield _deploy

    # delete the stacks in the reverse order they were created in case of inter-stack dependencies
    for stack_id, teardown in state[::-1]:
        try:
            teardown()
        except Exception as e:
            LOG.debug("Failed cleaning up stack stack_id=%s: %s", stack_id, e)


@pytest.fixture
def is_change_set_created_and_available(aws_client):
    def _is_change_set_created_and_available(change_set_id: str):
        def _inner():
            change_set = aws_client.cloudformation.describe_change_set(ChangeSetName=change_set_id)
            return (
                # TODO: CREATE_FAILED should also not lead to further retries
                change_set.get("Status") == "CREATE_COMPLETE"
                and change_set.get("ExecutionStatus") == "AVAILABLE"
            )

        return _inner

    return _is_change_set_created_and_available


@pytest.fixture
def is_change_set_failed_and_unavailable(aws_client):
    def _is_change_set_created_and_available(change_set_id: str):
        def _inner():
            change_set = aws_client.cloudformation.describe_change_set(ChangeSetName=change_set_id)
            return (
                # TODO: CREATE_FAILED should also not lead to further retries
                change_set.get("Status") == "FAILED"
                and change_set.get("ExecutionStatus") == "UNAVAILABLE"
            )

        return _inner

    return _is_change_set_created_and_available


@pytest.fixture
def is_stack_created(aws_client):
    return _has_stack_status(aws_client.cloudformation, ["CREATE_COMPLETE", "CREATE_FAILED"])


@pytest.fixture
def is_stack_updated(aws_client):
    return _has_stack_status(aws_client.cloudformation, ["UPDATE_COMPLETE", "UPDATE_FAILED"])


@pytest.fixture
def is_stack_deleted(aws_client):
    return _has_stack_status(aws_client.cloudformation, ["DELETE_COMPLETE"])


def _has_stack_status(cfn_client, statuses: List[str]):
    def _has_status(stack_id: str):
        def _inner():
            resp = cfn_client.describe_stacks(StackName=stack_id)
            s = resp["Stacks"][0]  # since the lookup  uses the id we can only get a single response
            return s.get("StackStatus") in statuses

        return _inner

    return _has_status


@pytest.fixture
def is_change_set_finished(aws_client):
    def _is_change_set_finished(change_set_id: str, stack_name: Optional[str] = None):
        def _inner():
            kwargs = {"ChangeSetName": change_set_id}
            if stack_name:
                kwargs["StackName"] = stack_name

            check_set = aws_client.cloudformation.describe_change_set(**kwargs)

            if check_set.get("ExecutionStatus") == "EXECUTE_FAILED":
                LOG.warning("Change set failed")
                raise ShortCircuitWaitException()

            return check_set.get("ExecutionStatus") == "EXECUTE_COMPLETE"

        return _inner

    return _is_change_set_finished


@pytest.fixture
def wait_until_lambda_ready(aws_client):
    def _wait_until_ready(function_name: str, qualifier: str = None, client=None):
        client = client or aws_client.lambda_

        def _is_not_pending():
            kwargs = {}
            if qualifier:
                kwargs["Qualifier"] = qualifier
            try:
                result = (
                    client.get_function(FunctionName=function_name)["Configuration"]["State"]
                    != "Pending"
                )
                LOG.debug("lambda state result: result=%s", result)
                return result
            except Exception as e:
                LOG.error(e)
                raise

        wait_until(_is_not_pending)

    return _wait_until_ready


role_assume_policy = """
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
""".strip()

role_policy = """
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
""".strip()


@pytest.fixture
def create_lambda_function_aws(aws_client):
    lambda_arns = []

    def _create_lambda_function(**kwargs):
        def _create_function():
            resp = aws_client.lambda_.create_function(**kwargs)
            lambda_arns.append(resp["FunctionArn"])

            def _is_not_pending():
                try:
                    result = (
                        aws_client.lambda_.get_function(FunctionName=resp["FunctionName"])[
                            "Configuration"
                        ]["State"]
                        != "Pending"
                    )
                    return result
                except Exception as e:
                    LOG.error(e)
                    raise

            wait_until(_is_not_pending)
            return resp

        # @AWS, takes about 10s until the role/policy is "active", until then it will fail
        # localstack should normally not require the retries and will just continue here
        return retry(_create_function, retries=3, sleep=4)

    yield _create_lambda_function

    for arn in lambda_arns:
        try:
            aws_client.lambda_.delete_function(FunctionName=arn)
        except Exception:
            LOG.debug("Unable to delete function arn=%s in cleanup", arn)


@pytest.fixture
def create_lambda_function(aws_client, wait_until_lambda_ready, lambda_su_role):
    lambda_arns_and_clients = []
    log_groups = []
    lambda_client = aws_client.lambda_
    logs_client = aws_client.logs
    s3_client = aws_client.s3

    def _create_lambda_function(*args, **kwargs):
        client = kwargs.get("client") or lambda_client
        kwargs["client"] = client
        kwargs["s3_client"] = s3_client
        func_name = kwargs.get("func_name")
        assert func_name
        del kwargs["func_name"]

        if not kwargs.get("role"):
            kwargs["role"] = lambda_su_role

        def _create_function():
            resp = testutil.create_lambda_function(func_name, **kwargs)
            lambda_arns_and_clients.append((resp["CreateFunctionResponse"]["FunctionArn"], client))
            wait_until_lambda_ready(function_name=func_name, client=client)
            log_group_name = f"/aws/lambda/{func_name}"
            log_groups.append(log_group_name)
            return resp

        # @AWS, takes about 10s until the role/policy is "active", until then it will fail
        # localstack should normally not require the retries and will just continue here
        return retry(_create_function, retries=3, sleep=4)

    yield _create_lambda_function

    for arn, client in lambda_arns_and_clients:
        try:
            client.delete_function(FunctionName=arn)
        except Exception:
            LOG.debug("Unable to delete function arn=%s in cleanup", arn)

    for log_group_name in log_groups:
        try:
            logs_client.delete_log_group(logGroupName=log_group_name)
        except Exception:
            LOG.debug("Unable to delete log group %s in cleanup", log_group_name)


@pytest.fixture
def create_echo_http_server(aws_client, create_lambda_function):
    from localstack.aws.api.lambda_ import Runtime

    lambda_client = aws_client.lambda_
    handler_code = textwrap.dedent(
        """
    import json
    import os


    def make_response(body: dict, status_code: int = 200):
        return {
            "statusCode": status_code,
            "headers": {"Content-Type": "application/json"},
            "body": body,
        }


    def trim_headers(headers):
        if not int(os.getenv("TRIM_X_HEADERS", 0)):
            return headers
        return {
            key: value for key, value in headers.items()
            if not (key.startswith("x-amzn") or key.startswith("x-forwarded-"))
        }


    def handler(event, context):
        print(json.dumps(event))
        response = {
            "args": event.get("queryStringParameters", {}),
            "data": event.get("body", ""),
            "domain": event["requestContext"].get("domainName", ""),
            "headers": trim_headers(event.get("headers", {})),
            "method": event["requestContext"]["http"].get("method", ""),
            "origin": event["requestContext"]["http"].get("sourceIp", ""),
            "path": event["requestContext"]["http"].get("path", ""),
        }
        return make_response(response)"""
    )

    def _create_echo_http_server(trim_x_headers: bool = False) -> str:
        """Creates a server that will echo any request. Any request will be returned with the
        following format. Any unset values will have those defaults.
        `trim_x_headers` can be set to True to trim some headers that are automatically added by lambda in
        order to create easier Snapshot testing. Default: `False`
        {
          "args": {},
          "headers": {},
          "data": "",
          "method": "",
          "domain": "",
          "origin": "",
          "path": ""
        }"""
        zip_file = testutil.create_lambda_archive(handler_code, get_content=True)
        func_name = f"echo-http-{short_uid()}"
        create_lambda_function(
            func_name=func_name,
            zip_file=zip_file,
            runtime=Runtime.python3_12,
            envvars={"TRIM_X_HEADERS": "1" if trim_x_headers else "0"},
        )
        url_response = lambda_client.create_function_url_config(
            FunctionName=func_name, AuthType="NONE"
        )
        aws_client.lambda_.add_permission(
            FunctionName=func_name,
            StatementId="urlPermission",
            Action="lambda:InvokeFunctionUrl",
            Principal="*",
            FunctionUrlAuthType="NONE",
        )
        return url_response["FunctionUrl"]

    yield _create_echo_http_server


@pytest.fixture
def create_event_source_mapping(aws_client):
    uuids = []

    def _create_event_source_mapping(*args, **kwargs):
        response = aws_client.lambda_.create_event_source_mapping(*args, **kwargs)
        uuids.append(response["UUID"])
        return response

    yield _create_event_source_mapping

    for uuid in uuids:
        try:
            aws_client.lambda_.delete_event_source_mapping(UUID=uuid)
        except Exception:
            LOG.debug("Unable to delete event source mapping %s in cleanup", uuid)


@pytest.fixture
def check_lambda_logs(aws_client):
    def _check_logs(func_name: str, expected_lines: List[str] = None) -> List[str]:
        if not expected_lines:
            expected_lines = []
        log_events = get_lambda_logs(func_name, logs_client=aws_client.logs)
        log_messages = [e["message"] for e in log_events]
        for line in expected_lines:
            if ".*" in line:
                found = [re.match(line, m, flags=re.DOTALL) for m in log_messages]
                if any(found):
                    continue
            assert line in log_messages
        return log_messages

    return _check_logs


@pytest.fixture
def create_policy(aws_client):
    policy_arns = []

    def _create_policy(*args, iam_client=None, **kwargs):
        iam_client = iam_client or aws_client.iam
        if "PolicyName" not in kwargs:
            kwargs["PolicyName"] = f"policy-{short_uid()}"
        response = iam_client.create_policy(*args, **kwargs)
        policy_arn = response["Policy"]["Arn"]
        policy_arns.append((policy_arn, iam_client))
        return response

    yield _create_policy

    for policy_arn, iam_client in policy_arns:
        try:
            iam_client.delete_policy(PolicyArn=policy_arn)
        except Exception:
            LOG.debug("Could not delete policy '%s' during test cleanup", policy_arn)


@pytest.fixture
def create_user(aws_client):
    usernames = []

    def _create_user(**kwargs):
        if "UserName" not in kwargs:
            kwargs["UserName"] = f"user-{short_uid()}"
        response = aws_client.iam.create_user(**kwargs)
        usernames.append(response["User"]["UserName"])
        return response

    yield _create_user

    for username in usernames:
        try:
            inline_policies = aws_client.iam.list_user_policies(UserName=username)["PolicyNames"]
        except ClientError as e:
            LOG.debug(
                "Cannot list user policies: %s. User %s probably already deleted...", e, username
            )
            continue

        for inline_policy in inline_policies:
            try:
                aws_client.iam.delete_user_policy(UserName=username, PolicyName=inline_policy)
            except Exception:
                LOG.debug(
                    "Could not delete user policy '%s' from '%s' during cleanup",
                    inline_policy,
                    username,
                )
        attached_policies = aws_client.iam.list_attached_user_policies(UserName=username)[
            "AttachedPolicies"
        ]
        for attached_policy in attached_policies:
            try:
                aws_client.iam.detach_user_policy(
                    UserName=username, PolicyArn=attached_policy["PolicyArn"]
                )
            except Exception:
                LOG.debug(
                    "Error detaching policy '%s' from user '%s'",
                    attached_policy["PolicyArn"],
                    username,
                )
        access_keys = aws_client.iam.list_access_keys(UserName=username)["AccessKeyMetadata"]
        for access_key in access_keys:
            try:
                aws_client.iam.delete_access_key(
                    UserName=username, AccessKeyId=access_key["AccessKeyId"]
                )
            except Exception:
                LOG.debug(
                    "Error deleting access key '%s' from user '%s'",
                    access_key["AccessKeyId"],
                    username,
                )

        try:
            aws_client.iam.delete_user(UserName=username)
        except Exception as e:
            LOG.debug("Error deleting user '%s' during test cleanup: %s", username, e)


@pytest.fixture
def wait_and_assume_role(aws_client):
    def _wait_and_assume_role(role_arn: str, session_name: str = None, **kwargs):
        if not session_name:
            session_name = f"session-{short_uid()}"

        def assume_role():
            return aws_client.sts.assume_role(
                RoleArn=role_arn, RoleSessionName=session_name, **kwargs
            )["Credentials"]

        # need to retry a couple of times before we are allowed to assume this role in AWS
        keys = retry(assume_role, sleep=5, retries=4)
        return keys

    return _wait_and_assume_role


@pytest.fixture
def create_role(aws_client):
    role_names = []

    def _create_role(iam_client=None, **kwargs):
        if not kwargs.get("RoleName"):
            kwargs["RoleName"] = f"role-{short_uid()}"
        iam_client = iam_client or aws_client.iam
        result = iam_client.create_role(**kwargs)
        role_names.append((result["Role"]["RoleName"], iam_client))
        return result

    yield _create_role

    for role_name, iam_client in role_names:
        # detach policies
        try:
            attached_policies = iam_client.list_attached_role_policies(RoleName=role_name)[
                "AttachedPolicies"
            ]
        except ClientError as e:
            LOG.debug(
                "Cannot list attached role policies: %s. Role %s probably already deleted...",
                e,
                role_name,
            )
            continue
        for attached_policy in attached_policies:
            try:
                iam_client.detach_role_policy(
                    RoleName=role_name, PolicyArn=attached_policy["PolicyArn"]
                )
            except Exception:
                LOG.debug(
                    "Could not detach role policy '%s' from '%s' during cleanup",
                    attached_policy["PolicyArn"],
                    role_name,
                )
        role_policies = iam_client.list_role_policies(RoleName=role_name)["PolicyNames"]
        for role_policy in role_policies:
            try:
                iam_client.delete_role_policy(RoleName=role_name, PolicyName=role_policy)
            except Exception:
                LOG.debug(
                    "Could not delete role policy '%s' from '%s' during cleanup",
                    role_policy,
                    role_name,
                )
        try:
            iam_client.delete_role(RoleName=role_name)
        except Exception:
            LOG.debug("Could not delete role '%s' during cleanup", role_name)


@pytest.fixture
def create_parameter(aws_client):
    params = []

    def _create_parameter(**kwargs):
        params.append(kwargs["Name"])
        return aws_client.ssm.put_parameter(**kwargs)

    yield _create_parameter

    for param in params:
        aws_client.ssm.delete_parameter(Name=param)


@pytest.fixture
def create_secret(aws_client):
    items = []

    def _create_parameter(**kwargs):
        create_response = aws_client.secretsmanager.create_secret(**kwargs)
        items.append(create_response["ARN"])
        return create_response

    yield _create_parameter

    for item in items:
        aws_client.secretsmanager.delete_secret(SecretId=item, ForceDeleteWithoutRecovery=True)


# TODO Figure out how to make cert creation tests pass against AWS.
#
# We would like to have localstack tests to pass not just against localstack, but also against AWS to make sure
# our emulation is correct. Unfortunately, with certificate creation there are some issues.
#
# In AWS newly created ACM certificates have to be validated either by email or by DNS. The latter is
# by adding some CNAME records as requested by ASW in response to a certificate request.
# For testing purposes the DNS one seems to be easier, at least as long as DNS is handled by Region53 AWS DNS service.
#
# The other possible option is to use IAM certificates instead of ACM ones. Those just have to be uploaded from files
# created by openssl etc. Not sure if there are other issues after that.
#
# The third option might be having in AWS some certificates created in advance - so they do not require validation
# and can be easily used in tests. The issie with such an approach is that for AppSync, for example, in order to
# register a domain name (https://docs.aws.amazon.com/appsync/latest/APIReference/API_CreateDomainName.html),
# the domain name in the API request has to match the domain name used in certificate creation. Which means that with
# pre-created certificates we would have to use specific domain names instead of random ones.
@pytest.fixture
def acm_request_certificate(aws_client_factory):
    certificate_arns = []

    def factory(**kwargs) -> str:
        if "DomainName" not in kwargs:
            kwargs["DomainName"] = f"test-domain-{short_uid()}.localhost.localstack.cloud"

        region_name = kwargs.pop("region_name", None)
        acm_client = aws_client_factory(region_name=region_name).acm

        response = acm_client.request_certificate(**kwargs)
        created_certificate_arn = response["CertificateArn"]
        certificate_arns.append((created_certificate_arn, region_name))
        return response

    yield factory

    # cleanup
    for certificate_arn, region_name in certificate_arns:
        try:
            acm_client = aws_client_factory(region_name=region_name).acm
            acm_client.delete_certificate(CertificateArn=certificate_arn)
        except Exception as e:
            LOG.debug("error cleaning up certificate %s: %s", certificate_arn, e)


role_policy_su = {
    "Version": "2012-10-17",
    "Statement": [{"Effect": "Allow", "Action": ["*"], "Resource": ["*"]}],
}


@pytest.fixture(scope="session")
def lambda_su_role(aws_client):
    role_name = f"lambda-autogenerated-{short_uid()}"
    role = aws_client.iam.create_role(
        RoleName=role_name, AssumeRolePolicyDocument=role_assume_policy
    )["Role"]
    policy_name = f"lambda-autogenerated-{short_uid()}"
    policy_arn = aws_client.iam.create_policy(
        PolicyName=policy_name, PolicyDocument=json.dumps(role_policy_su)
    )["Policy"]["Arn"]
    aws_client.iam.attach_role_policy(RoleName=role_name, PolicyArn=policy_arn)

    if is_aws_cloud():  # dirty but necessary
        time.sleep(10)

    yield role["Arn"]

    run_safe(aws_client.iam.detach_role_policy(RoleName=role_name, PolicyArn=policy_arn))
    run_safe(aws_client.iam.delete_role(RoleName=role_name))
    run_safe(aws_client.iam.delete_policy(PolicyArn=policy_arn))


@pytest.fixture
def create_iam_role_and_attach_policy(aws_client):
    """
    Fixture that creates an IAM role with given role definition and predefined policy ARN.

    Use this fixture with AWS managed policies like 'AmazonS3ReadOnlyAccess' or 'AmazonKinesisFullAccess'.
    """
    roles = []

    def _inner(**kwargs: dict[str, any]) -> str:
        """
        :param dict RoleDefinition: role definition document
        :param str PolicyArn: policy ARN
        :param str RoleName: role name (autogenerated if omitted)
        :return: role ARN
        """
        if "RoleName" not in kwargs:
            kwargs["RoleName"] = f"test-role-{short_uid()}"

        role = kwargs["RoleName"]
        role_policy = json.dumps(kwargs["RoleDefinition"])

        result = aws_client.iam.create_role(RoleName=role, AssumeRolePolicyDocument=role_policy)
        role_arn = result["Role"]["Arn"]

        policy_arn = kwargs["PolicyArn"]
        aws_client.iam.attach_role_policy(PolicyArn=policy_arn, RoleName=role)

        roles.append(role)
        return role_arn

    yield _inner

    for role in roles:
        try:
            aws_client.iam.delete_role(RoleName=role)
        except Exception as exc:
            LOG.debug("Error deleting IAM role '%s': %s", role, exc)


@pytest.fixture
def create_iam_role_with_policy(aws_client):
    """
    Fixture that creates an IAM role with given role definition and policy definition.
    """
    roles = {}

    def _create_role_and_policy(**kwargs: dict[str, any]) -> str:
        """
        :param dict RoleDefinition: role definition document
        :param dict PolicyDefinition: policy definition document
        :param str PolicyName: policy name (autogenerated if omitted)
        :param str RoleName: role name (autogenerated if omitted)
        :return: role ARN
        """
        if "RoleName" not in kwargs:
            kwargs["RoleName"] = f"test-role-{short_uid()}"
        role = kwargs["RoleName"]
        if "PolicyName" not in kwargs:
            kwargs["PolicyName"] = f"test-policy-{short_uid()}"
        policy = kwargs["PolicyName"]
        role_policy = json.dumps(kwargs["RoleDefinition"])

        result = aws_client.iam.create_role(RoleName=role, AssumeRolePolicyDocument=role_policy)
        role_arn = result["Role"]["Arn"]

        policy_document = json.dumps(kwargs["PolicyDefinition"])
        aws_client.iam.put_role_policy(
            RoleName=role, PolicyName=policy, PolicyDocument=policy_document
        )
        roles[role] = policy
        return role_arn

    yield _create_role_and_policy

    for role_name, policy_name in roles.items():
        try:
            aws_client.iam.delete_role_policy(RoleName=role_name, PolicyName=policy_name)
        except Exception as exc:
            LOG.debug("Error deleting IAM role policy '%s' '%s': %s", role_name, policy_name, exc)
        try:
            aws_client.iam.delete_role(RoleName=role_name)
        except Exception as exc:
            LOG.debug("Error deleting IAM role '%s': %s", role_name, exc)


@pytest.fixture
def firehose_create_delivery_stream(wait_for_delivery_stream_ready, aws_client):
    delivery_stream_names = []

    def _create_delivery_stream(**kwargs):
        if "DeliveryStreamName" not in kwargs:
            kwargs["DeliveryStreamName"] = f"test-delivery-stream-{short_uid()}"
        delivery_stream_name = kwargs["DeliveryStreamName"]
        response = aws_client.firehose.create_delivery_stream(**kwargs)
        delivery_stream_names.append(delivery_stream_name)
        wait_for_delivery_stream_ready(delivery_stream_name)
        return response

    yield _create_delivery_stream

    for delivery_stream_name in delivery_stream_names:
        try:
            aws_client.firehose.delete_delivery_stream(DeliveryStreamName=delivery_stream_name)
        except Exception:
            LOG.info("Failed to delete delivery stream %s", delivery_stream_name)


@pytest.fixture
def ses_configuration_set(aws_client):
    configuration_set_names = []

    def factory(name: str) -> None:
        aws_client.ses.create_configuration_set(
            ConfigurationSet={
                "Name": name,
            },
        )
        configuration_set_names.append(name)

    yield factory

    for configuration_set_name in configuration_set_names:
        aws_client.ses.delete_configuration_set(ConfigurationSetName=configuration_set_name)


@pytest.fixture
def ses_configuration_set_sns_event_destination(aws_client):
    event_destinations = []

    def factory(config_set_name: str, event_destination_name: str, topic_arn: str) -> None:
        aws_client.ses.create_configuration_set_event_destination(
            ConfigurationSetName=config_set_name,
            EventDestination={
                "Name": event_destination_name,
                "Enabled": True,
                "MatchingEventTypes": ["send", "bounce", "delivery", "open", "click"],
                "SNSDestination": {
                    "TopicARN": topic_arn,
                },
            },
        )
        event_destinations.append((config_set_name, event_destination_name))

    yield factory

    for created_config_set_name, created_event_destination_name in event_destinations:
        aws_client.ses.delete_configuration_set_event_destination(
            ConfigurationSetName=created_config_set_name,
            EventDestinationName=created_event_destination_name,
        )


@pytest.fixture
def ses_email_template(aws_client):
    template_names = []

    def factory(name: str, contents: str, subject: str = f"Email template {short_uid()}"):
        aws_client.ses.create_template(
            Template={
                "TemplateName": name,
                "SubjectPart": subject,
                "TextPart": contents,
            }
        )
        template_names.append(name)

    yield factory

    for template_name in template_names:
        aws_client.ses.delete_template(TemplateName=template_name)


@pytest.fixture
def ses_verify_identity(aws_client):
    identities = []

    def factory(email_address: str) -> None:
        aws_client.ses.verify_email_identity(EmailAddress=email_address)

    yield factory

    for identity in identities:
        aws_client.ses.delete_identity(Identity=identity)


@pytest.fixture
def setup_sender_email_address(ses_verify_identity):
    """
    If the test is running against AWS then assume the email address passed is already
    verified, and passes the given email address through. Otherwise, it generates one random
    email address and verify them.
    """

    def inner(sender_email_address: Optional[str] = None) -> str:
        if is_aws_cloud():
            if sender_email_address is None:
                raise ValueError(
                    "sender_email_address must be specified to run this test against AWS"
                )
        else:
            # overwrite the given parameters with localstack specific ones
            sender_email_address = f"sender-{short_uid()}@example.com"
            ses_verify_identity(sender_email_address)

        return sender_email_address

    return inner


@pytest.fixture
def ec2_create_security_group(aws_client):
    ec2_sgs = []

    def factory(ports=None, ip_protocol: str = "tcp", **kwargs):
        """
        Create the target group and authorize the security group ingress.
        :param ports: list of ports to be authorized for the ingress rule.
        :param ip_protocol: the ip protocol for the permissions (tcp by default)
        """
        if "GroupName" not in kwargs:
            # FIXME: This will fail against AWS since the sg prefix is not valid for GroupName
            # > "Group names may not be in the format sg-*".
            kwargs["GroupName"] = f"sg-{short_uid()}"
        # Making sure the call to CreateSecurityGroup gets the right arguments
        _args = select_from_typed_dict(CreateSecurityGroupRequest, kwargs)
        security_group = aws_client.ec2.create_security_group(**_args)
        security_group_id = security_group["GroupId"]

        # FIXME: If 'ports' is None or an empty list, authorize_security_group_ingress will fail due to missing IpPermissions.
        # Must ensure ports are explicitly provided or skip authorization entirely if not required.
        permissions = [
            {
                "FromPort": port,
                "IpProtocol": ip_protocol,
                "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                "ToPort": port,
            }
            for port in ports or []
        ]
        aws_client.ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=permissions,
        )

        ec2_sgs.append(security_group_id)
        return security_group

    yield factory

    for sg_group_id in ec2_sgs:
        try:
            aws_client.ec2.delete_security_group(GroupId=sg_group_id)
        except Exception as e:
            LOG.debug("Error cleaning up EC2 security group: %s, %s", sg_group_id, e)


@pytest.fixture
def ec2_create_vpc_endpoint(aws_client):
    vpc_endpoints = []

    def _create(**kwargs: Unpack[CreateVpcEndpointRequest]) -> VpcEndpoint:
        endpoint = aws_client.ec2.create_vpc_endpoint(**kwargs)
        endpoint_id = endpoint["VpcEndpoint"]["VpcEndpointId"]
        vpc_endpoints.append(endpoint_id)

        def _check_available() -> VpcEndpoint:
            result = aws_client.ec2.describe_vpc_endpoints(VpcEndpointIds=[endpoint_id])
            _endpoint_details = result["VpcEndpoints"][0]
            assert _endpoint_details["State"] == "available"

            return _endpoint_details

        return retry(_check_available, retries=30, sleep=5 if is_aws_cloud() else 1)

    yield _create

    try:
        aws_client.ec2.delete_vpc_endpoints(VpcEndpointIds=vpc_endpoints)
    except Exception as e:
        LOG.error("Error cleaning up VPC endpoint: %s, %s", vpc_endpoints, e)

    def wait_for_endpoint_deleted():
        try:
            endpoints = aws_client.ec2.describe_vpc_endpoints(VpcEndpointIds=vpc_endpoints)
            assert len(endpoints["VpcEndpoints"]) == 0 or all(
                endpoint["State"] == "Deleted" for endpoint in endpoints["VpcEndpoints"]
            )
        except botocore.exceptions.ClientError:
            pass

    # the vpc can't be deleted if an endpoint exists
    if is_aws_cloud():
        retry(wait_for_endpoint_deleted, retries=30, sleep=10 if is_aws_cloud() else 1)


@pytest.fixture
def cleanups():
    cleanup_fns = []

    yield cleanup_fns

    for cleanup_callback in cleanup_fns[::-1]:
        try:
            cleanup_callback()
        except Exception as e:
            LOG.warning("Failed to execute cleanup", exc_info=e)


@pytest.fixture(scope="session")
def account_id(aws_client):
    if is_aws_cloud() or is_api_enabled("sts"):
        return aws_client.sts.get_caller_identity()["Account"]
    else:
        return TEST_AWS_ACCOUNT_ID


@pytest.fixture(scope="session")
def region_name(aws_client):
    if is_aws_cloud() or is_api_enabled("sts"):
        return aws_client.sts.meta.region_name
    else:
        return TEST_AWS_REGION_NAME


@pytest.fixture(scope="session")
def partition(region_name):
    return get_partition(region_name)


@pytest.fixture(scope="session")
def secondary_account_id(secondary_aws_client):
    if is_aws_cloud() or is_api_enabled("sts"):
        return secondary_aws_client.sts.get_caller_identity()["Account"]
    else:
        return SECONDARY_TEST_AWS_ACCOUNT_ID


@pytest.fixture(scope="session")
def secondary_region_name():
    return SECONDARY_TEST_AWS_REGION_NAME


@pytest.hookimpl
def pytest_collection_modifyitems(config: Config, items: list[Item]):
    only_localstack = pytest.mark.skipif(
        is_aws_cloud(),
        reason="test only applicable if run against localstack",
    )
    for item in items:
        for mark in item.iter_markers():
            if mark.name.endswith("only_localstack"):
                item.add_marker(only_localstack)
        if hasattr(item, "fixturenames") and "snapshot" in item.fixturenames:
            # add a marker that indicates that this test is snapshot validated
            # if it uses the snapshot fixture -> allows selecting only snapshot
            # validated tests in order to capture new snapshots for a whole
            # test file with "-m snapshot_validated"
            item.add_marker("snapshot_validated")


@pytest.fixture
def sample_stores() -> AccountRegionBundle:
    class SampleStore(BaseStore):
        CROSS_ACCOUNT_ATTR = CrossAccountAttribute(default=list)
        CROSS_REGION_ATTR = CrossRegionAttribute(default=list)
        region_specific_attr = LocalAttribute(default=list)

    return AccountRegionBundle("zzz", SampleStore, validate=False)


@pytest.fixture
def create_rest_apigw(aws_client_factory):
    rest_apis = []
    retry_boto_config = None
    if is_aws_cloud():
        retry_boto_config = botocore.config.Config(
            # Api gateway can throttle requests pretty heavily. Leading to potentially undeleted apis
            retries={"max_attempts": 10, "mode": "adaptive"}
        )

    def _create_apigateway_function(**kwargs):
        client_region_name = kwargs.pop("region_name", None)
        apigateway_client = aws_client_factory(
            region_name=client_region_name, config=retry_boto_config
        ).apigateway
        kwargs.setdefault("name", f"api-{short_uid()}")

        response = apigateway_client.create_rest_api(**kwargs)
        api_id = response.get("id")
        rest_apis.append((api_id, client_region_name))

        return api_id, response.get("name"), response.get("rootResourceId")

    yield _create_apigateway_function

    for rest_api_id, _client_region_name in rest_apis:
        apigateway_client = aws_client_factory(
            region_name=_client_region_name,
            config=retry_boto_config,
        ).apigateway
        # First, retrieve the usage plans associated with the REST API
        usage_plan_ids = []
        usage_plans = apigateway_client.get_usage_plans()
        for item in usage_plans.get("items", []):
            api_stages = item.get("apiStages", [])
            usage_plan_ids.extend(
                item.get("id") for api_stage in api_stages if api_stage.get("apiId") == rest_api_id
            )

        # Then delete the API, as you can't delete the UsagePlan if a stage is associated with it
        with contextlib.suppress(Exception):
            apigateway_client.delete_rest_api(restApiId=rest_api_id)

        # finally delete the usage plans and the API Keys linked to it
        for usage_plan_id in usage_plan_ids:
            usage_plan_keys = apigateway_client.get_usage_plan_keys(usagePlanId=usage_plan_id)
            for key in usage_plan_keys.get("items", []):
                apigateway_client.delete_api_key(apiKey=key["id"])
            apigateway_client.delete_usage_plan(usagePlanId=usage_plan_id)


@pytest.fixture
def create_rest_apigw_openapi(aws_client_factory):
    rest_apis = []

    def _create_apigateway_function(**kwargs):
        region_name = kwargs.pop("region_name", None)
        apigateway_client = aws_client_factory(region_name=region_name).apigateway

        response = apigateway_client.import_rest_api(**kwargs)
        api_id = response.get("id")
        rest_apis.append((api_id, region_name))
        return api_id, response

    yield _create_apigateway_function

    for rest_api_id, region_name in rest_apis:
        with contextlib.suppress(Exception):
            apigateway_client = aws_client_factory(region_name=region_name).apigateway
            apigateway_client.delete_rest_api(restApiId=rest_api_id)


@pytest.fixture
def assert_host_customisation(monkeypatch):
    localstack_host = "foo.bar"
    monkeypatch.setattr(
        config, "LOCALSTACK_HOST", config.HostAndPort(host=localstack_host, port=8888)
    )

    def asserter(
        url: str,
        *,
        custom_host: Optional[str] = None,
    ):
        if custom_host is not None:
            assert custom_host in url, f"Could not find `{custom_host}` in `{url}`"

            assert localstack_host not in url
        else:
            assert localstack_host in url, f"Could not find `{localstack_host}` in `{url}`"

    yield asserter


@pytest.fixture
def echo_http_server(httpserver: HTTPServer):
    """Spins up a local HTTP echo server and returns the endpoint URL"""

    def _echo(request: Request) -> Response:
        request_json = None
        if request.is_json:
            with contextlib.suppress(ValueError):
                request_json = json.loads(request.data)
        result = {
            "data": request.data or "{}",
            "headers": dict(request.headers),
            "url": request.url,
            "method": request.method,
            "json": request_json,
        }
        response_body = json.dumps(json_safe(result))
        return Response(response_body, status=200)

    httpserver.expect_request("").respond_with_handler(_echo)
    http_endpoint = httpserver.url_for("/")

    return http_endpoint


@pytest.fixture
def echo_http_server_post(echo_http_server):
    """
    Returns an HTTP echo server URL for POST requests that work both locally and for parity tests (against real AWS)
    """
    if is_aws_cloud():
        return f"{PUBLIC_HTTP_ECHO_SERVER_URL}/post"

    return f"{echo_http_server}post"


def create_policy_doc(effect: str, actions: List, resource=None) -> Dict:
    actions = ensure_list(actions)
    resource = resource or "*"
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                # TODO statement ids have to be alphanumeric [0-9A-Za-z], write a test for it
                "Sid": f"s{short_uid()}",
                "Effect": effect,
                "Action": actions,
                "Resource": resource,
            }
        ],
    }


@pytest.fixture
def create_policy_generated_document(create_policy):
    def _create_policy_with_doc(effect, actions, policy_name=None, resource=None, iam_client=None):
        policy_name = policy_name or f"p-{short_uid()}"
        policy = create_policy_doc(effect, actions, resource=resource)
        response = create_policy(
            PolicyName=policy_name, PolicyDocument=json.dumps(policy), iam_client=iam_client
        )
        policy_arn = response["Policy"]["Arn"]
        return policy_arn

    return _create_policy_with_doc


@pytest.fixture
def create_role_with_policy(create_role, create_policy_generated_document, aws_client):
    def _create_role_with_policy(
        effect, actions, assume_policy_doc, resource=None, attach=True, iam_client=None
    ):
        iam_client = iam_client or aws_client.iam

        role_name = f"role-{short_uid()}"
        result = create_role(
            RoleName=role_name, AssumeRolePolicyDocument=assume_policy_doc, iam_client=iam_client
        )
        role_arn = result["Role"]["Arn"]
        policy_name = f"p-{short_uid()}"

        if attach:
            # create role and attach role policy
            policy_arn = create_policy_generated_document(
                effect, actions, policy_name=policy_name, resource=resource, iam_client=iam_client
            )
            iam_client.attach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
        else:
            # put role policy
            policy_document = create_policy_doc(effect, actions, resource=resource)
            policy_document = json.dumps(policy_document)
            iam_client.put_role_policy(
                RoleName=role_name, PolicyName=policy_name, PolicyDocument=policy_document
            )

        return role_name, role_arn

    return _create_role_with_policy


@pytest.fixture
def create_user_with_policy(create_policy_generated_document, create_user, aws_client):
    def _create_user_with_policy(effect, actions, resource=None):
        policy_arn = create_policy_generated_document(effect, actions, resource=resource)
        username = f"user-{short_uid()}"
        create_user(UserName=username)
        aws_client.iam.attach_user_policy(UserName=username, PolicyArn=policy_arn)
        keys = aws_client.iam.create_access_key(UserName=username)["AccessKey"]
        return username, keys

    return _create_user_with_policy


@pytest.fixture()
def register_extension(s3_bucket, aws_client):
    cfn_client = aws_client.cloudformation
    extensions_arns = []

    def _register(extension_name, extension_type, artifact_path):
        bucket = s3_bucket
        key = f"artifact-{short_uid()}"

        aws_client.s3.upload_file(artifact_path, bucket, key)

        register_response = cfn_client.register_type(
            Type=extension_type,
            TypeName=extension_name,
            SchemaHandlerPackage=f"s3://{bucket}/{key}",
        )

        registration_token = register_response["RegistrationToken"]
        cfn_client.get_waiter("type_registration_complete").wait(
            RegistrationToken=registration_token
        )

        describe_response = cfn_client.describe_type_registration(
            RegistrationToken=registration_token
        )

        extensions_arns.append(describe_response["TypeArn"])
        cfn_client.set_type_default_version(Arn=describe_response["TypeVersionArn"])

        return describe_response

    yield _register

    for arn in extensions_arns:
        versions = cfn_client.list_type_versions(Arn=arn)["TypeVersionSummaries"]
        for v in versions:
            try:
                cfn_client.deregister_type(Arn=v["Arn"])
            except Exception:
                continue
        cfn_client.deregister_type(Arn=arn)


@pytest.fixture
def hosted_zone(aws_client):
    zone_ids = []

    def factory(**kwargs):
        if "CallerReference" not in kwargs:
            kwargs["CallerReference"] = f"ref-{short_uid()}"
        response = aws_client.route53.create_hosted_zone(**kwargs)
        zone_id = response["HostedZone"]["Id"]
        zone_ids.append(zone_id)
        return response

    yield factory

    for zone_id in zone_ids[::-1]:
        aws_client.route53.delete_hosted_zone(Id=zone_id)


@pytest.fixture
def openapi_validate(monkeypatch):
    monkeypatch.setattr(config, "OPENAPI_VALIDATE_RESPONSE", "true")
    monkeypatch.setattr(config, "OPENAPI_VALIDATE_REQUEST", "true")


@pytest.fixture
def set_resource_custom_id():
    set_ids = []

    def _set_custom_id(resource_identifier: ResourceIdentifier, custom_id):
        localstack_id_manager.set_custom_id(
            resource_identifier=resource_identifier, custom_id=custom_id
        )
        set_ids.append(resource_identifier)

    yield _set_custom_id

    for resource_identifier in set_ids:
        localstack_id_manager.unset_custom_id(resource_identifier)


###############################
# Events (EventBridge) fixtures
###############################


@pytest.fixture
def events_create_event_bus(aws_client, region_name, account_id):
    event_bus_names = []

    def _create_event_bus(**kwargs):
        if "Name" not in kwargs:
            kwargs["Name"] = f"test-event-bus-{short_uid()}"

        response = aws_client.events.create_event_bus(**kwargs)
        event_bus_names.append(kwargs["Name"])
        return response

    yield _create_event_bus

    for event_bus_name in event_bus_names:
        try:
            response = aws_client.events.list_rules(EventBusName=event_bus_name)
            rules = [rule["Name"] for rule in response["Rules"]]

            # Delete all rules for the current event bus
            for rule in rules:
                try:
                    response = aws_client.events.list_targets_by_rule(
                        Rule=rule, EventBusName=event_bus_name
                    )
                    targets = [target["Id"] for target in response["Targets"]]

                    # Remove all targets for the current rule
                    if targets:
                        for target in targets:
                            aws_client.events.remove_targets(
                                Rule=rule, EventBusName=event_bus_name, Ids=[target]
                            )

                    aws_client.events.delete_rule(Name=rule, EventBusName=event_bus_name)
                except Exception as e:
                    LOG.warning("Failed to delete rule %s: %s", rule, e)

            # Delete archives for event bus
            event_source_arn = (
                f"arn:aws:events:{region_name}:{account_id}:event-bus/{event_bus_name}"
            )
            response = aws_client.events.list_archives(EventSourceArn=event_source_arn)
            archives = [archive["ArchiveName"] for archive in response["Archives"]]
            for archive in archives:
                try:
                    aws_client.events.delete_archive(ArchiveName=archive)
                except Exception as e:
                    LOG.warning("Failed to delete archive %s: %s", archive, e)

            aws_client.events.delete_event_bus(Name=event_bus_name)
        except Exception as e:
            LOG.warning("Failed to delete event bus %s: %s", event_bus_name, e)


@pytest.fixture
def events_put_rule(aws_client):
    rules = []

    def _put_rule(**kwargs):
        if "Name" not in kwargs:
            kwargs["Name"] = f"rule-{short_uid()}"

        response = aws_client.events.put_rule(**kwargs)
        rules.append((kwargs["Name"], kwargs.get("EventBusName", "default")))
        return response

    yield _put_rule

    for rule, event_bus_name in rules:
        try:
            response = aws_client.events.list_targets_by_rule(
                Rule=rule, EventBusName=event_bus_name
            )
            targets = [target["Id"] for target in response["Targets"]]

            # Remove all targets for the current rule
            if targets:
                for target in targets:
                    aws_client.events.remove_targets(
                        Rule=rule, EventBusName=event_bus_name, Ids=[target]
                    )

            aws_client.events.delete_rule(Name=rule, EventBusName=event_bus_name)
        except Exception as e:
            LOG.warning("Failed to delete rule %s: %s", rule, e)


@pytest.fixture
def events_create_rule(aws_client):
    rules = []

    def _create_rule(**kwargs):
        rule_name = kwargs["Name"]
        bus_name = kwargs.get("EventBusName", "")
        pattern = kwargs.get("EventPattern", {})
        schedule = kwargs.get("ScheduleExpression", "")
        rule_arn = aws_client.events.put_rule(
            Name=rule_name,
            EventBusName=bus_name,
            EventPattern=json.dumps(pattern),
            ScheduleExpression=schedule,
        )["RuleArn"]
        rules.append({"name": rule_name, "bus": bus_name})
        return rule_arn

    yield _create_rule

    for rule in rules:
        targets = aws_client.events.list_targets_by_rule(
            Rule=rule["name"], EventBusName=rule["bus"]
        )["Targets"]

        targetIds = [target["Id"] for target in targets]
        if len(targetIds) > 0:
            aws_client.events.remove_targets(
                Rule=rule["name"], EventBusName=rule["bus"], Ids=targetIds
            )

        aws_client.events.delete_rule(Name=rule["name"], EventBusName=rule["bus"])


@pytest.fixture
def sqs_as_events_target(aws_client, sqs_get_queue_arn):
    queue_urls = []

    def _sqs_as_events_target(queue_name: str | None = None) -> tuple[str, str]:
        if not queue_name:
            queue_name = f"tests-queue-{short_uid()}"
        sqs_client = aws_client.sqs
        queue_url = sqs_client.create_queue(QueueName=queue_name)["QueueUrl"]
        queue_urls.append(queue_url)
        queue_arn = sqs_get_queue_arn(queue_url)
        policy = {
            "Version": "2012-10-17",
            "Id": f"sqs-eventbridge-{short_uid()}",
            "Statement": [
                {
                    "Sid": f"SendMessage-{short_uid()}",
                    "Effect": "Allow",
                    "Principal": {"Service": "events.amazonaws.com"},
                    "Action": "sqs:SendMessage",
                    "Resource": queue_arn,
                }
            ],
        }
        sqs_client.set_queue_attributes(
            QueueUrl=queue_url, Attributes={"Policy": json.dumps(policy)}
        )
        return queue_url, queue_arn

    yield _sqs_as_events_target

    for queue_url in queue_urls:
        try:
            aws_client.sqs.delete_queue(QueueUrl=queue_url)
        except Exception as e:
            LOG.debug("error cleaning up queue %s: %s", queue_url, e)


@pytest.fixture
def clean_up(
    aws_client,
):  # TODO: legacy clean up fixtures for eventbridge - remove and use individual fixtures for creating resources instead
    def _clean_up(
        bus_name=None,
        rule_name=None,
        target_ids=None,
        queue_url=None,
        log_group_name=None,
    ):
        events_client = aws_client.events
        kwargs = {"EventBusName": bus_name} if bus_name else {}
        if target_ids:
            target_ids = target_ids if isinstance(target_ids, list) else [target_ids]
            call_safe(
                events_client.remove_targets,
                kwargs=dict(Rule=rule_name, Ids=target_ids, Force=True, **kwargs),
            )
        if rule_name:
            call_safe(events_client.delete_rule, kwargs=dict(Name=rule_name, Force=True, **kwargs))
        if bus_name:
            call_safe(events_client.delete_event_bus, kwargs=dict(Name=bus_name))
        if queue_url:
            sqs_client = aws_client.sqs
            call_safe(sqs_client.delete_queue, kwargs=dict(QueueUrl=queue_url))
        if log_group_name:
            logs_client = aws_client.logs

            def _delete_log_group():
                log_streams = logs_client.describe_log_streams(logGroupName=log_group_name)
                for log_stream in log_streams["logStreams"]:
                    logs_client.delete_log_stream(
                        logGroupName=log_group_name, logStreamName=log_stream["logStreamName"]
                    )
                logs_client.delete_log_group(logGroupName=log_group_name)

            call_safe(_delete_log_group)

    yield _clean_up


@pytest.fixture(params=["dill", "jsonpickle"])
def patch_default_encoder(request, monkeypatch):
    backend = request.param
    monkeypatch.setattr(config, "STATE_SERIALIZATION_BACKEND", backend)
