from datetime import datetime
from enum import StrEnum
from typing import IO, Dict, Iterable, Iterator, List, Optional, TypedDict, Union

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

AbortRuleId = str
AcceptRanges = str
AccessKeyIdValue = str
AccessPointAlias = bool
AccessPointArn = str
AccountId = str
AllowQuotedRecordDelimiter = bool
AllowedHeader = str
AllowedMethod = str
AllowedOrigin = str
AnalyticsId = str
BucketKeyEnabled = bool
BucketLocationName = str
BucketName = str
BucketRegion = str
BypassGovernanceRetention = bool
CacheControl = str
ChecksumCRC32 = str
ChecksumCRC32C = str
ChecksumCRC64NVME = str
ChecksumSHA1 = str
ChecksumSHA256 = str
ClientToken = str
CloudFunction = str
CloudFunctionInvocationRole = str
Code = str
Comments = str
ConfirmRemoveSelfBucketAccess = bool
ContentDisposition = str
ContentEncoding = str
ContentLanguage = str
ContentMD5 = str
ContentRange = str
ContentType = str
CopySource = str
CopySourceIfMatch = str
CopySourceIfNoneMatch = str
CopySourceRange = str
CopySourceSSECustomerAlgorithm = str
CopySourceSSECustomerKey = str
CopySourceSSECustomerKeyMD5 = str
CopySourceVersionId = str
Days = int
DaysAfterInitiation = int
DeleteMarker = bool
DeleteMarkerVersionId = str
Delimiter = str
Description = str
DirectoryBucketToken = str
DisplayName = str
ETag = str
EmailAddress = str
EnableRequestProgress = bool
ErrorCode = str
ErrorMessage = str
Expiration = str
ExpiredObjectDeleteMarker = bool
ExposeHeader = str
Expression = str
FetchOwner = bool
FieldDelimiter = str
FilterRuleValue = str
GetObjectResponseStatusCode = int
GrantFullControl = str
GrantRead = str
GrantReadACP = str
GrantWrite = str
GrantWriteACP = str
HostName = str
HttpErrorCodeReturnedEquals = str
HttpRedirectCode = str
ID = str
IfMatch = str
IfNoneMatch = str
IntelligentTieringDays = int
IntelligentTieringId = str
InventoryId = str
IsEnabled = bool
IsLatest = bool
IsPublic = bool
IsRestoreInProgress = bool
IsTruncated = bool
KMSContext = str
KeyCount = int
KeyMarker = str
KeyPrefixEquals = str
KmsKeyArn = str
LambdaFunctionArn = str
Location = str
LocationNameAsString = str
LocationPrefix = str
MFA = str
Marker = str
MaxAgeSeconds = int
MaxBuckets = int
MaxDirectoryBuckets = int
MaxKeys = int
MaxParts = int
MaxUploads = int
Message = str
MetadataKey = str
MetadataTableStatus = str
MetadataValue = str
MetricsId = str
Minutes = int
MissingMeta = int
MultipartUploadId = str
NextKeyMarker = str
NextMarker = str
NextPartNumberMarker = int
NextToken = str
NextUploadIdMarker = str
NextVersionIdMarker = str
NotificationId = str
ObjectKey = str
ObjectLockEnabledForBucket = bool
ObjectLockToken = str
ObjectVersionId = str
PartNumber = int
PartNumberMarker = int
PartsCount = int
Policy = str
Prefix = str
Priority = int
QueueArn = str
Quiet = bool
QuoteCharacter = str
QuoteEscapeCharacter = str
Range = str
RecordDelimiter = str
RecordExpirationDays = int
Region = str
RenameSource = str
RenameSourceIfMatch = str
RenameSourceIfNoneMatch = str
ReplaceKeyPrefixWith = str
ReplaceKeyWith = str
ReplicaKmsKeyID = str
RequestRoute = str
RequestToken = str
ResponseCacheControl = str
ResponseContentDisposition = str
ResponseContentEncoding = str
ResponseContentLanguage = str
ResponseContentType = str
Restore = str
RestoreOutputPath = str
Role = str
S3RegionalOrS3ExpressBucketArnString = str
S3TablesArn = str
S3TablesBucketArn = str
S3TablesName = str
S3TablesNamespace = str
SSECustomerAlgorithm = str
SSECustomerKey = str
SSECustomerKeyMD5 = str
SSEKMSEncryptionContext = str
SSEKMSKeyId = str
SessionCredentialValue = str
Setting = bool
SkipValidation = bool
StartAfter = str
Suffix = str
TagCount = int
TaggingHeader = str
TargetBucket = str
TargetPrefix = str
Token = str
TopicArn = str
URI = str
UploadIdMarker = str
Value = str
VersionCount = int
VersionIdMarker = str
WebsiteRedirectLocation = str
Years = int
BucketContentType = str
IfCondition = str
RestoreObjectOutputStatusCode = int
ArgumentName = str
ArgumentValue = str
AWSAccessKeyId = str
HostId = str
HeadersNotSigned = str
SignatureProvided = str
StringToSign = str
StringToSignBytes = str
CanonicalRequest = str
CanonicalRequestBytes = str
X_Amz_Expires = int
HttpMethod = str
ResourceType = str
MissingHeaderName = str
KeyLength = str
Header = str
additionalMessage = str


class AnalyticsS3ExportFileFormat(StrEnum):
    CSV = "CSV"


class ArchiveStatus(StrEnum):
    ARCHIVE_ACCESS = "ARCHIVE_ACCESS"
    DEEP_ARCHIVE_ACCESS = "DEEP_ARCHIVE_ACCESS"


class BucketAccelerateStatus(StrEnum):
    Enabled = "Enabled"
    Suspended = "Suspended"


class BucketCannedACL(StrEnum):
    private = "private"
    public_read = "public-read"
    public_read_write = "public-read-write"
    authenticated_read = "authenticated-read"
    log_delivery_write = "log-delivery-write"


class BucketLocationConstraint(StrEnum):
    af_south_1 = "af-south-1"
    ap_east_1 = "ap-east-1"
    ap_northeast_1 = "ap-northeast-1"
    ap_northeast_2 = "ap-northeast-2"
    ap_northeast_3 = "ap-northeast-3"
    ap_south_1 = "ap-south-1"
    ap_south_2 = "ap-south-2"
    ap_southeast_1 = "ap-southeast-1"
    ap_southeast_2 = "ap-southeast-2"
    ap_southeast_3 = "ap-southeast-3"
    ap_southeast_4 = "ap-southeast-4"
    ap_southeast_5 = "ap-southeast-5"
    ca_central_1 = "ca-central-1"
    cn_north_1 = "cn-north-1"
    cn_northwest_1 = "cn-northwest-1"
    EU = "EU"
    eu_central_1 = "eu-central-1"
    eu_central_2 = "eu-central-2"
    eu_north_1 = "eu-north-1"
    eu_south_1 = "eu-south-1"
    eu_south_2 = "eu-south-2"
    eu_west_1 = "eu-west-1"
    eu_west_2 = "eu-west-2"
    eu_west_3 = "eu-west-3"
    il_central_1 = "il-central-1"
    me_central_1 = "me-central-1"
    me_south_1 = "me-south-1"
    sa_east_1 = "sa-east-1"
    us_east_2 = "us-east-2"
    us_gov_east_1 = "us-gov-east-1"
    us_gov_west_1 = "us-gov-west-1"
    us_west_1 = "us-west-1"
    us_west_2 = "us-west-2"


class BucketLogsPermission(StrEnum):
    FULL_CONTROL = "FULL_CONTROL"
    READ = "READ"
    WRITE = "WRITE"


class BucketType(StrEnum):
    Directory = "Directory"


class BucketVersioningStatus(StrEnum):
    Enabled = "Enabled"
    Suspended = "Suspended"


class ChecksumAlgorithm(StrEnum):
    CRC32 = "CRC32"
    CRC32C = "CRC32C"
    SHA1 = "SHA1"
    SHA256 = "SHA256"
    CRC64NVME = "CRC64NVME"


class ChecksumMode(StrEnum):
    ENABLED = "ENABLED"


class ChecksumType(StrEnum):
    COMPOSITE = "COMPOSITE"
    FULL_OBJECT = "FULL_OBJECT"


class CompressionType(StrEnum):
    NONE = "NONE"
    GZIP = "GZIP"
    BZIP2 = "BZIP2"


class DataRedundancy(StrEnum):
    SingleAvailabilityZone = "SingleAvailabilityZone"
    SingleLocalZone = "SingleLocalZone"


class DeleteMarkerReplicationStatus(StrEnum):
    Enabled = "Enabled"
    Disabled = "Disabled"


class EncodingType(StrEnum):
    url = "url"


class Event(StrEnum):
    s3_ReducedRedundancyLostObject = "s3:ReducedRedundancyLostObject"
    s3_ObjectCreated_ = "s3:ObjectCreated:*"
    s3_ObjectCreated_Put = "s3:ObjectCreated:Put"
    s3_ObjectCreated_Post = "s3:ObjectCreated:Post"
    s3_ObjectCreated_Copy = "s3:ObjectCreated:Copy"
    s3_ObjectCreated_CompleteMultipartUpload = "s3:ObjectCreated:CompleteMultipartUpload"
    s3_ObjectRemoved_ = "s3:ObjectRemoved:*"
    s3_ObjectRemoved_Delete = "s3:ObjectRemoved:Delete"
    s3_ObjectRemoved_DeleteMarkerCreated = "s3:ObjectRemoved:DeleteMarkerCreated"
    s3_ObjectRestore_ = "s3:ObjectRestore:*"
    s3_ObjectRestore_Post = "s3:ObjectRestore:Post"
    s3_ObjectRestore_Completed = "s3:ObjectRestore:Completed"
    s3_Replication_ = "s3:Replication:*"
    s3_Replication_OperationFailedReplication = "s3:Replication:OperationFailedReplication"
    s3_Replication_OperationNotTracked = "s3:Replication:OperationNotTracked"
    s3_Replication_OperationMissedThreshold = "s3:Replication:OperationMissedThreshold"
    s3_Replication_OperationReplicatedAfterThreshold = (
        "s3:Replication:OperationReplicatedAfterThreshold"
    )
    s3_ObjectRestore_Delete = "s3:ObjectRestore:Delete"
    s3_LifecycleTransition = "s3:LifecycleTransition"
    s3_IntelligentTiering = "s3:IntelligentTiering"
    s3_ObjectAcl_Put = "s3:ObjectAcl:Put"
    s3_LifecycleExpiration_ = "s3:LifecycleExpiration:*"
    s3_LifecycleExpiration_Delete = "s3:LifecycleExpiration:Delete"
    s3_LifecycleExpiration_DeleteMarkerCreated = "s3:LifecycleExpiration:DeleteMarkerCreated"
    s3_ObjectTagging_ = "s3:ObjectTagging:*"
    s3_ObjectTagging_Put = "s3:ObjectTagging:Put"
    s3_ObjectTagging_Delete = "s3:ObjectTagging:Delete"


class ExistingObjectReplicationStatus(StrEnum):
    Enabled = "Enabled"
    Disabled = "Disabled"


class ExpirationState(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class ExpirationStatus(StrEnum):
    Enabled = "Enabled"
    Disabled = "Disabled"


class ExpressionType(StrEnum):
    SQL = "SQL"


class FileHeaderInfo(StrEnum):
    USE = "USE"
    IGNORE = "IGNORE"
    NONE = "NONE"


class FilterRuleName(StrEnum):
    prefix = "prefix"
    suffix = "suffix"


class IntelligentTieringAccessTier(StrEnum):
    ARCHIVE_ACCESS = "ARCHIVE_ACCESS"
    DEEP_ARCHIVE_ACCESS = "DEEP_ARCHIVE_ACCESS"


class IntelligentTieringStatus(StrEnum):
    Enabled = "Enabled"
    Disabled = "Disabled"


class InventoryConfigurationState(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class InventoryFormat(StrEnum):
    CSV = "CSV"
    ORC = "ORC"
    Parquet = "Parquet"


class InventoryFrequency(StrEnum):
    Daily = "Daily"
    Weekly = "Weekly"


class InventoryIncludedObjectVersions(StrEnum):
    All = "All"
    Current = "Current"


class InventoryOptionalField(StrEnum):
    Size = "Size"
    LastModifiedDate = "LastModifiedDate"
    StorageClass = "StorageClass"
    ETag = "ETag"
    IsMultipartUploaded = "IsMultipartUploaded"
    ReplicationStatus = "ReplicationStatus"
    EncryptionStatus = "EncryptionStatus"
    ObjectLockRetainUntilDate = "ObjectLockRetainUntilDate"
    ObjectLockMode = "ObjectLockMode"
    ObjectLockLegalHoldStatus = "ObjectLockLegalHoldStatus"
    IntelligentTieringAccessTier = "IntelligentTieringAccessTier"
    BucketKeyStatus = "BucketKeyStatus"
    ChecksumAlgorithm = "ChecksumAlgorithm"
    ObjectAccessControlList = "ObjectAccessControlList"
    ObjectOwner = "ObjectOwner"


class JSONType(StrEnum):
    DOCUMENT = "DOCUMENT"
    LINES = "LINES"


class LocationType(StrEnum):
    AvailabilityZone = "AvailabilityZone"
    LocalZone = "LocalZone"


class MFADelete(StrEnum):
    Enabled = "Enabled"
    Disabled = "Disabled"


class MFADeleteStatus(StrEnum):
    Enabled = "Enabled"
    Disabled = "Disabled"


class MetadataDirective(StrEnum):
    COPY = "COPY"
    REPLACE = "REPLACE"


class MetricsStatus(StrEnum):
    Enabled = "Enabled"
    Disabled = "Disabled"


class ObjectAttributes(StrEnum):
    ETag = "ETag"
    Checksum = "Checksum"
    ObjectParts = "ObjectParts"
    StorageClass = "StorageClass"
    ObjectSize = "ObjectSize"


class ObjectCannedACL(StrEnum):
    private = "private"
    public_read = "public-read"
    public_read_write = "public-read-write"
    authenticated_read = "authenticated-read"
    aws_exec_read = "aws-exec-read"
    bucket_owner_read = "bucket-owner-read"
    bucket_owner_full_control = "bucket-owner-full-control"


class ObjectLockEnabled(StrEnum):
    Enabled = "Enabled"


class ObjectLockLegalHoldStatus(StrEnum):
    ON = "ON"
    OFF = "OFF"


class ObjectLockMode(StrEnum):
    GOVERNANCE = "GOVERNANCE"
    COMPLIANCE = "COMPLIANCE"


class ObjectLockRetentionMode(StrEnum):
    GOVERNANCE = "GOVERNANCE"
    COMPLIANCE = "COMPLIANCE"


class ObjectOwnership(StrEnum):
    BucketOwnerPreferred = "BucketOwnerPreferred"
    ObjectWriter = "ObjectWriter"
    BucketOwnerEnforced = "BucketOwnerEnforced"


class ObjectStorageClass(StrEnum):
    STANDARD = "STANDARD"
    REDUCED_REDUNDANCY = "REDUCED_REDUNDANCY"
    GLACIER = "GLACIER"
    STANDARD_IA = "STANDARD_IA"
    ONEZONE_IA = "ONEZONE_IA"
    INTELLIGENT_TIERING = "INTELLIGENT_TIERING"
    DEEP_ARCHIVE = "DEEP_ARCHIVE"
    OUTPOSTS = "OUTPOSTS"
    GLACIER_IR = "GLACIER_IR"
    SNOW = "SNOW"
    EXPRESS_ONEZONE = "EXPRESS_ONEZONE"
    FSX_OPENZFS = "FSX_OPENZFS"


class ObjectVersionStorageClass(StrEnum):
    STANDARD = "STANDARD"


class OptionalObjectAttributes(StrEnum):
    RestoreStatus = "RestoreStatus"


class OwnerOverride(StrEnum):
    Destination = "Destination"


class PartitionDateSource(StrEnum):
    EventTime = "EventTime"
    DeliveryTime = "DeliveryTime"


class Payer(StrEnum):
    Requester = "Requester"
    BucketOwner = "BucketOwner"


class Permission(StrEnum):
    FULL_CONTROL = "FULL_CONTROL"
    WRITE = "WRITE"
    WRITE_ACP = "WRITE_ACP"
    READ = "READ"
    READ_ACP = "READ_ACP"


class Protocol(StrEnum):
    http = "http"
    https = "https"


class QuoteFields(StrEnum):
    ALWAYS = "ALWAYS"
    ASNEEDED = "ASNEEDED"


class ReplicaModificationsStatus(StrEnum):
    Enabled = "Enabled"
    Disabled = "Disabled"


class ReplicationRuleStatus(StrEnum):
    Enabled = "Enabled"
    Disabled = "Disabled"


class ReplicationStatus(StrEnum):
    COMPLETE = "COMPLETE"
    PENDING = "PENDING"
    FAILED = "FAILED"
    REPLICA = "REPLICA"
    COMPLETED = "COMPLETED"


class ReplicationTimeStatus(StrEnum):
    Enabled = "Enabled"
    Disabled = "Disabled"


class RequestCharged(StrEnum):
    requester = "requester"


class RequestPayer(StrEnum):
    requester = "requester"


class RestoreRequestType(StrEnum):
    SELECT = "SELECT"


class S3TablesBucketType(StrEnum):
    aws = "aws"
    customer = "customer"


class ServerSideEncryption(StrEnum):
    AES256 = "AES256"
    aws_fsx = "aws:fsx"
    aws_kms = "aws:kms"
    aws_kms_dsse = "aws:kms:dsse"


class SessionMode(StrEnum):
    ReadOnly = "ReadOnly"
    ReadWrite = "ReadWrite"


class SseKmsEncryptedObjectsStatus(StrEnum):
    Enabled = "Enabled"
    Disabled = "Disabled"


class StorageClass(StrEnum):
    STANDARD = "STANDARD"
    REDUCED_REDUNDANCY = "REDUCED_REDUNDANCY"
    STANDARD_IA = "STANDARD_IA"
    ONEZONE_IA = "ONEZONE_IA"
    INTELLIGENT_TIERING = "INTELLIGENT_TIERING"
    GLACIER = "GLACIER"
    DEEP_ARCHIVE = "DEEP_ARCHIVE"
    OUTPOSTS = "OUTPOSTS"
    GLACIER_IR = "GLACIER_IR"
    SNOW = "SNOW"
    EXPRESS_ONEZONE = "EXPRESS_ONEZONE"
    FSX_OPENZFS = "FSX_OPENZFS"


class StorageClassAnalysisSchemaVersion(StrEnum):
    V_1 = "V_1"


class TableSseAlgorithm(StrEnum):
    aws_kms = "aws:kms"
    AES256 = "AES256"


class TaggingDirective(StrEnum):
    COPY = "COPY"
    REPLACE = "REPLACE"


class Tier(StrEnum):
    Standard = "Standard"
    Bulk = "Bulk"
    Expedited = "Expedited"


class TransitionDefaultMinimumObjectSize(StrEnum):
    varies_by_storage_class = "varies_by_storage_class"
    all_storage_classes_128K = "all_storage_classes_128K"


class TransitionStorageClass(StrEnum):
    GLACIER = "GLACIER"
    STANDARD_IA = "STANDARD_IA"
    ONEZONE_IA = "ONEZONE_IA"
    INTELLIGENT_TIERING = "INTELLIGENT_TIERING"
    DEEP_ARCHIVE = "DEEP_ARCHIVE"
    GLACIER_IR = "GLACIER_IR"


class Type(StrEnum):
    CanonicalUser = "CanonicalUser"
    AmazonCustomerByEmail = "AmazonCustomerByEmail"
    Group = "Group"


class BucketAlreadyExists(ServiceException):
    code: str = "BucketAlreadyExists"
    sender_fault: bool = False
    status_code: int = 409


class BucketAlreadyOwnedByYou(ServiceException):
    code: str = "BucketAlreadyOwnedByYou"
    sender_fault: bool = False
    status_code: int = 409
    BucketName: Optional[BucketName]


class EncryptionTypeMismatch(ServiceException):
    code: str = "EncryptionTypeMismatch"
    sender_fault: bool = False
    status_code: int = 400


class IdempotencyParameterMismatch(ServiceException):
    code: str = "IdempotencyParameterMismatch"
    sender_fault: bool = False
    status_code: int = 400


class InvalidObjectState(ServiceException):
    code: str = "InvalidObjectState"
    sender_fault: bool = False
    status_code: int = 403
    StorageClass: Optional[StorageClass]
    AccessTier: Optional[IntelligentTieringAccessTier]


class InvalidRequest(ServiceException):
    code: str = "InvalidRequest"
    sender_fault: bool = False
    status_code: int = 400


class InvalidWriteOffset(ServiceException):
    code: str = "InvalidWriteOffset"
    sender_fault: bool = False
    status_code: int = 400


class NoSuchBucket(ServiceException):
    code: str = "NoSuchBucket"
    sender_fault: bool = False
    status_code: int = 404
    BucketName: Optional[BucketName]


class NoSuchKey(ServiceException):
    code: str = "NoSuchKey"
    sender_fault: bool = False
    status_code: int = 404
    Key: Optional[ObjectKey]
    DeleteMarker: Optional[DeleteMarker]
    VersionId: Optional[ObjectVersionId]


class NoSuchUpload(ServiceException):
    code: str = "NoSuchUpload"
    sender_fault: bool = False
    status_code: int = 404
    UploadId: Optional[MultipartUploadId]


class ObjectAlreadyInActiveTierError(ServiceException):
    code: str = "ObjectAlreadyInActiveTierError"
    sender_fault: bool = False
    status_code: int = 403


class ObjectNotInActiveTierError(ServiceException):
    code: str = "ObjectNotInActiveTierError"
    sender_fault: bool = False
    status_code: int = 403


class TooManyParts(ServiceException):
    code: str = "TooManyParts"
    sender_fault: bool = False
    status_code: int = 400


class NoSuchLifecycleConfiguration(ServiceException):
    code: str = "NoSuchLifecycleConfiguration"
    sender_fault: bool = False
    status_code: int = 404
    BucketName: Optional[BucketName]


class InvalidBucketName(ServiceException):
    code: str = "InvalidBucketName"
    sender_fault: bool = False
    status_code: int = 400
    BucketName: Optional[BucketName]


class NoSuchVersion(ServiceException):
    code: str = "NoSuchVersion"
    sender_fault: bool = False
    status_code: int = 404
    VersionId: Optional[ObjectVersionId]
    Key: Optional[ObjectKey]


class PreconditionFailed(ServiceException):
    code: str = "PreconditionFailed"
    sender_fault: bool = False
    status_code: int = 412
    Condition: Optional[IfCondition]


ObjectSize = int


class InvalidRange(ServiceException):
    code: str = "InvalidRange"
    sender_fault: bool = False
    status_code: int = 416
    ActualObjectSize: Optional[ObjectSize]
    RangeRequested: Optional[ContentRange]


class InvalidArgument(ServiceException):
    code: str = "InvalidArgument"
    sender_fault: bool = False
    status_code: int = 400
    ArgumentName: Optional[ArgumentName]
    ArgumentValue: Optional[ArgumentValue]
    HostId: Optional[HostId]


class SignatureDoesNotMatch(ServiceException):
    code: str = "SignatureDoesNotMatch"
    sender_fault: bool = False
    status_code: int = 403
    AWSAccessKeyId: Optional[AWSAccessKeyId]
    CanonicalRequest: Optional[CanonicalRequest]
    CanonicalRequestBytes: Optional[CanonicalRequestBytes]
    HostId: Optional[HostId]
    SignatureProvided: Optional[SignatureProvided]
    StringToSign: Optional[StringToSign]
    StringToSignBytes: Optional[StringToSignBytes]


ServerTime = datetime
Expires = datetime


class AccessDenied(ServiceException):
    code: str = "AccessDenied"
    sender_fault: bool = False
    status_code: int = 403
    Expires: Optional[Expires]
    ServerTime: Optional[ServerTime]
    X_Amz_Expires: Optional[X_Amz_Expires]
    HostId: Optional[HostId]
    HeadersNotSigned: Optional[HeadersNotSigned]


class AuthorizationQueryParametersError(ServiceException):
    code: str = "AuthorizationQueryParametersError"
    sender_fault: bool = False
    status_code: int = 400
    HostId: Optional[HostId]


class NoSuchWebsiteConfiguration(ServiceException):
    code: str = "NoSuchWebsiteConfiguration"
    sender_fault: bool = False
    status_code: int = 404
    BucketName: Optional[BucketName]


class ReplicationConfigurationNotFoundError(ServiceException):
    code: str = "ReplicationConfigurationNotFoundError"
    sender_fault: bool = False
    status_code: int = 404
    BucketName: Optional[BucketName]


class BadRequest(ServiceException):
    code: str = "BadRequest"
    sender_fault: bool = False
    status_code: int = 400
    HostId: Optional[HostId]


class AccessForbidden(ServiceException):
    code: str = "AccessForbidden"
    sender_fault: bool = False
    status_code: int = 403
    HostId: Optional[HostId]
    Method: Optional[HttpMethod]
    ResourceType: Optional[ResourceType]


class NoSuchCORSConfiguration(ServiceException):
    code: str = "NoSuchCORSConfiguration"
    sender_fault: bool = False
    status_code: int = 404
    BucketName: Optional[BucketName]


class MissingSecurityHeader(ServiceException):
    code: str = "MissingSecurityHeader"
    sender_fault: bool = False
    status_code: int = 400
    MissingHeaderName: Optional[MissingHeaderName]


class InvalidPartOrder(ServiceException):
    code: str = "InvalidPartOrder"
    sender_fault: bool = False
    status_code: int = 400
    UploadId: Optional[MultipartUploadId]


class InvalidStorageClass(ServiceException):
    code: str = "InvalidStorageClass"
    sender_fault: bool = False
    status_code: int = 400
    StorageClassRequested: Optional[StorageClass]


class MethodNotAllowed(ServiceException):
    code: str = "MethodNotAllowed"
    sender_fault: bool = False
    status_code: int = 405
    Method: Optional[HttpMethod]
    ResourceType: Optional[ResourceType]
    DeleteMarker: Optional[DeleteMarker]
    VersionId: Optional[ObjectVersionId]
    Allow: Optional[HttpMethod]


class CrossLocationLoggingProhibitted(ServiceException):
    code: str = "CrossLocationLoggingProhibitted"
    sender_fault: bool = False
    status_code: int = 403
    TargetBucketLocation: Optional[BucketRegion]
    SourceBucketLocation: Optional[BucketRegion]


class InvalidTargetBucketForLogging(ServiceException):
    code: str = "InvalidTargetBucketForLogging"
    sender_fault: bool = False
    status_code: int = 400
    TargetBucket: Optional[BucketName]


class BucketNotEmpty(ServiceException):
    code: str = "BucketNotEmpty"
    sender_fault: bool = False
    status_code: int = 409
    BucketName: Optional[BucketName]


ProposedSize = int
MinSizeAllowed = int


class EntityTooSmall(ServiceException):
    code: str = "EntityTooSmall"
    sender_fault: bool = False
    status_code: int = 400
    ETag: Optional[ETag]
    MinSizeAllowed: Optional[MinSizeAllowed]
    PartNumber: Optional[PartNumber]
    ProposedSize: Optional[ProposedSize]


class InvalidPart(ServiceException):
    code: str = "InvalidPart"
    sender_fault: bool = False
    status_code: int = 400
    ETag: Optional[ETag]
    UploadId: Optional[MultipartUploadId]
    PartNumber: Optional[PartNumber]


class NoSuchTagSet(ServiceException):
    code: str = "NoSuchTagSet"
    sender_fault: bool = False
    status_code: int = 404
    BucketName: Optional[BucketName]


class InvalidTag(ServiceException):
    code: str = "InvalidTag"
    sender_fault: bool = False
    status_code: int = 400
    TagKey: Optional[ObjectKey]
    TagValue: Optional[Value]


class ObjectLockConfigurationNotFoundError(ServiceException):
    code: str = "ObjectLockConfigurationNotFoundError"
    sender_fault: bool = False
    status_code: int = 404
    BucketName: Optional[BucketName]


class InvalidPartNumber(ServiceException):
    code: str = "InvalidPartNumber"
    sender_fault: bool = False
    status_code: int = 416
    PartNumberRequested: Optional[PartNumber]
    ActualPartCount: Optional[PartNumber]


class OwnershipControlsNotFoundError(ServiceException):
    code: str = "OwnershipControlsNotFoundError"
    sender_fault: bool = False
    status_code: int = 404
    BucketName: Optional[BucketName]


class NoSuchPublicAccessBlockConfiguration(ServiceException):
    code: str = "NoSuchPublicAccessBlockConfiguration"
    sender_fault: bool = False
    status_code: int = 404
    BucketName: Optional[BucketName]


class NoSuchBucketPolicy(ServiceException):
    code: str = "NoSuchBucketPolicy"
    sender_fault: bool = False
    status_code: int = 404
    BucketName: Optional[BucketName]


class InvalidDigest(ServiceException):
    code: str = "InvalidDigest"
    sender_fault: bool = False
    status_code: int = 400
    Content_MD5: Optional[ContentMD5]


class KeyTooLongError(ServiceException):
    code: str = "KeyTooLongError"
    sender_fault: bool = False
    status_code: int = 400
    MaxSizeAllowed: Optional[KeyLength]
    Size: Optional[KeyLength]


class InvalidLocationConstraint(ServiceException):
    code: str = "InvalidLocationConstraint"
    sender_fault: bool = False
    status_code: int = 400
    LocationConstraint: Optional[BucketRegion]


class EntityTooLarge(ServiceException):
    code: str = "EntityTooLarge"
    sender_fault: bool = False
    status_code: int = 400
    MaxSizeAllowed: Optional[KeyLength]
    HostId: Optional[HostId]
    ProposedSize: Optional[ProposedSize]


class InvalidEncryptionAlgorithmError(ServiceException):
    code: str = "InvalidEncryptionAlgorithmError"
    sender_fault: bool = False
    status_code: int = 400
    ArgumentName: Optional[ArgumentName]
    ArgumentValue: Optional[ArgumentValue]


class NotImplemented(ServiceException):
    code: str = "NotImplemented"
    sender_fault: bool = False
    status_code: int = 501
    Header: Optional[Header]
    additionalMessage: Optional[additionalMessage]


class ConditionalRequestConflict(ServiceException):
    code: str = "ConditionalRequestConflict"
    sender_fault: bool = False
    status_code: int = 409
    Condition: Optional[IfCondition]
    Key: Optional[ObjectKey]


class BadDigest(ServiceException):
    code: str = "BadDigest"
    sender_fault: bool = False
    status_code: int = 400
    ExpectedDigest: Optional[ContentMD5]
    CalculatedDigest: Optional[ContentMD5]


AbortDate = datetime


class AbortIncompleteMultipartUpload(TypedDict, total=False):
    DaysAfterInitiation: Optional[DaysAfterInitiation]


class AbortMultipartUploadOutput(TypedDict, total=False):
    RequestCharged: Optional[RequestCharged]


IfMatchInitiatedTime = datetime


class AbortMultipartUploadRequest(ServiceRequest):
    Bucket: BucketName
    Key: ObjectKey
    UploadId: MultipartUploadId
    RequestPayer: Optional[RequestPayer]
    ExpectedBucketOwner: Optional[AccountId]
    IfMatchInitiatedTime: Optional[IfMatchInitiatedTime]


class AccelerateConfiguration(TypedDict, total=False):
    Status: Optional[BucketAccelerateStatus]


class Owner(TypedDict, total=False):
    DisplayName: Optional[DisplayName]
    ID: Optional[ID]


class Grantee(TypedDict, total=False):
    DisplayName: Optional[DisplayName]
    EmailAddress: Optional[EmailAddress]
    ID: Optional[ID]
    Type: Type
    URI: Optional[URI]


class Grant(TypedDict, total=False):
    Grantee: Optional[Grantee]
    Permission: Optional[Permission]


Grants = List[Grant]


class AccessControlPolicy(TypedDict, total=False):
    Grants: Optional[Grants]
    Owner: Optional[Owner]


class AccessControlTranslation(TypedDict, total=False):
    Owner: OwnerOverride


AllowedHeaders = List[AllowedHeader]
AllowedMethods = List[AllowedMethod]
AllowedOrigins = List[AllowedOrigin]


class Tag(TypedDict, total=False):
    Key: ObjectKey
    Value: Value


TagSet = List[Tag]


class AnalyticsAndOperator(TypedDict, total=False):
    Prefix: Optional[Prefix]
    Tags: Optional[TagSet]


class AnalyticsS3BucketDestination(TypedDict, total=False):
    Format: AnalyticsS3ExportFileFormat
    BucketAccountId: Optional[AccountId]
    Bucket: BucketName
    Prefix: Optional[Prefix]


class AnalyticsExportDestination(TypedDict, total=False):
    S3BucketDestination: AnalyticsS3BucketDestination


class StorageClassAnalysisDataExport(TypedDict, total=False):
    OutputSchemaVersion: StorageClassAnalysisSchemaVersion
    Destination: AnalyticsExportDestination


class StorageClassAnalysis(TypedDict, total=False):
    DataExport: Optional[StorageClassAnalysisDataExport]


class AnalyticsFilter(TypedDict, total=False):
    Prefix: Optional[Prefix]
    Tag: Optional[Tag]
    And: Optional[AnalyticsAndOperator]


class AnalyticsConfiguration(TypedDict, total=False):
    Id: AnalyticsId
    Filter: Optional[AnalyticsFilter]
    StorageClassAnalysis: StorageClassAnalysis


AnalyticsConfigurationList = List[AnalyticsConfiguration]
Body = bytes
CreationDate = datetime


class Bucket(TypedDict, total=False):
    Name: Optional[BucketName]
    CreationDate: Optional[CreationDate]
    BucketRegion: Optional[BucketRegion]
    BucketArn: Optional[S3RegionalOrS3ExpressBucketArnString]


class BucketInfo(TypedDict, total=False):
    DataRedundancy: Optional[DataRedundancy]
    Type: Optional[BucketType]


class NoncurrentVersionExpiration(TypedDict, total=False):
    NoncurrentDays: Optional[Days]
    NewerNoncurrentVersions: Optional[VersionCount]


class NoncurrentVersionTransition(TypedDict, total=False):
    NoncurrentDays: Optional[Days]
    StorageClass: Optional[TransitionStorageClass]
    NewerNoncurrentVersions: Optional[VersionCount]


NoncurrentVersionTransitionList = List[NoncurrentVersionTransition]
Date = datetime


class Transition(TypedDict, total=False):
    Date: Optional[Date]
    Days: Optional[Days]
    StorageClass: Optional[TransitionStorageClass]


TransitionList = List[Transition]
ObjectSizeLessThanBytes = int
ObjectSizeGreaterThanBytes = int


class LifecycleRuleAndOperator(TypedDict, total=False):
    Prefix: Optional[Prefix]
    Tags: Optional[TagSet]
    ObjectSizeGreaterThan: Optional[ObjectSizeGreaterThanBytes]
    ObjectSizeLessThan: Optional[ObjectSizeLessThanBytes]


class LifecycleRuleFilter(TypedDict, total=False):
    Prefix: Optional[Prefix]
    Tag: Optional[Tag]
    ObjectSizeGreaterThan: Optional[ObjectSizeGreaterThanBytes]
    ObjectSizeLessThan: Optional[ObjectSizeLessThanBytes]
    And: Optional[LifecycleRuleAndOperator]


class LifecycleExpiration(TypedDict, total=False):
    Date: Optional[Date]
    Days: Optional[Days]
    ExpiredObjectDeleteMarker: Optional[ExpiredObjectDeleteMarker]


class LifecycleRule(TypedDict, total=False):
    Expiration: Optional[LifecycleExpiration]
    ID: Optional[ID]
    Prefix: Optional[Prefix]
    Filter: Optional[LifecycleRuleFilter]
    Status: ExpirationStatus
    Transitions: Optional[TransitionList]
    NoncurrentVersionTransitions: Optional[NoncurrentVersionTransitionList]
    NoncurrentVersionExpiration: Optional[NoncurrentVersionExpiration]
    AbortIncompleteMultipartUpload: Optional[AbortIncompleteMultipartUpload]


LifecycleRules = List[LifecycleRule]


class BucketLifecycleConfiguration(TypedDict, total=False):
    Rules: LifecycleRules


class PartitionedPrefix(TypedDict, total=False):
    PartitionDateSource: Optional[PartitionDateSource]


class SimplePrefix(TypedDict, total=False):
    pass


class TargetObjectKeyFormat(TypedDict, total=False):
    SimplePrefix: Optional[SimplePrefix]
    PartitionedPrefix: Optional[PartitionedPrefix]


class TargetGrant(TypedDict, total=False):
    Grantee: Optional[Grantee]
    Permission: Optional[BucketLogsPermission]


TargetGrants = List[TargetGrant]


class LoggingEnabled(TypedDict, total=False):
    TargetBucket: TargetBucket
    TargetGrants: Optional[TargetGrants]
    TargetPrefix: TargetPrefix
    TargetObjectKeyFormat: Optional[TargetObjectKeyFormat]


class BucketLoggingStatus(TypedDict, total=False):
    LoggingEnabled: Optional[LoggingEnabled]


Buckets = List[Bucket]
BytesProcessed = int
BytesReturned = int
BytesScanned = int
ExposeHeaders = List[ExposeHeader]


class CORSRule(TypedDict, total=False):
    ID: Optional[ID]
    AllowedHeaders: Optional[AllowedHeaders]
    AllowedMethods: AllowedMethods
    AllowedOrigins: AllowedOrigins
    ExposeHeaders: Optional[ExposeHeaders]
    MaxAgeSeconds: Optional[MaxAgeSeconds]


CORSRules = List[CORSRule]


class CORSConfiguration(TypedDict, total=False):
    CORSRules: CORSRules


class CSVInput(TypedDict, total=False):
    FileHeaderInfo: Optional[FileHeaderInfo]
    Comments: Optional[Comments]
    QuoteEscapeCharacter: Optional[QuoteEscapeCharacter]
    RecordDelimiter: Optional[RecordDelimiter]
    FieldDelimiter: Optional[FieldDelimiter]
    QuoteCharacter: Optional[QuoteCharacter]
    AllowQuotedRecordDelimiter: Optional[AllowQuotedRecordDelimiter]


class CSVOutput(TypedDict, total=False):
    QuoteFields: Optional[QuoteFields]
    QuoteEscapeCharacter: Optional[QuoteEscapeCharacter]
    RecordDelimiter: Optional[RecordDelimiter]
    FieldDelimiter: Optional[FieldDelimiter]
    QuoteCharacter: Optional[QuoteCharacter]


class Checksum(TypedDict, total=False):
    ChecksumCRC32: Optional[ChecksumCRC32]
    ChecksumCRC32C: Optional[ChecksumCRC32C]
    ChecksumCRC64NVME: Optional[ChecksumCRC64NVME]
    ChecksumSHA1: Optional[ChecksumSHA1]
    ChecksumSHA256: Optional[ChecksumSHA256]
    ChecksumType: Optional[ChecksumType]


ChecksumAlgorithmList = List[ChecksumAlgorithm]
EventList = List[Event]


class CloudFunctionConfiguration(TypedDict, total=False):
    Id: Optional[NotificationId]
    Event: Optional[Event]
    Events: Optional[EventList]
    CloudFunction: Optional[CloudFunction]
    InvocationRole: Optional[CloudFunctionInvocationRole]


class CommonPrefix(TypedDict, total=False):
    Prefix: Optional[Prefix]


CommonPrefixList = List[CommonPrefix]


class CompleteMultipartUploadOutput(TypedDict, total=False):
    Location: Optional[Location]
    Bucket: Optional[BucketName]
    Key: Optional[ObjectKey]
    Expiration: Optional[Expiration]
    ETag: Optional[ETag]
    ChecksumCRC32: Optional[ChecksumCRC32]
    ChecksumCRC32C: Optional[ChecksumCRC32C]
    ChecksumCRC64NVME: Optional[ChecksumCRC64NVME]
    ChecksumSHA1: Optional[ChecksumSHA1]
    ChecksumSHA256: Optional[ChecksumSHA256]
    ChecksumType: Optional[ChecksumType]
    ServerSideEncryption: Optional[ServerSideEncryption]
    VersionId: Optional[ObjectVersionId]
    SSEKMSKeyId: Optional[SSEKMSKeyId]
    BucketKeyEnabled: Optional[BucketKeyEnabled]
    RequestCharged: Optional[RequestCharged]


MpuObjectSize = int


class CompletedPart(TypedDict, total=False):
    ETag: Optional[ETag]
    ChecksumCRC32: Optional[ChecksumCRC32]
    ChecksumCRC32C: Optional[ChecksumCRC32C]
    ChecksumCRC64NVME: Optional[ChecksumCRC64NVME]
    ChecksumSHA1: Optional[ChecksumSHA1]
    ChecksumSHA256: Optional[ChecksumSHA256]
    PartNumber: Optional[PartNumber]


CompletedPartList = List[CompletedPart]


class CompletedMultipartUpload(TypedDict, total=False):
    Parts: Optional[CompletedPartList]


class CompleteMultipartUploadRequest(ServiceRequest):
    Bucket: BucketName
    Key: ObjectKey
    MultipartUpload: Optional[CompletedMultipartUpload]
    UploadId: MultipartUploadId
    ChecksumCRC32: Optional[ChecksumCRC32]
    ChecksumCRC32C: Optional[ChecksumCRC32C]
    ChecksumCRC64NVME: Optional[ChecksumCRC64NVME]
    ChecksumSHA1: Optional[ChecksumSHA1]
    ChecksumSHA256: Optional[ChecksumSHA256]
    ChecksumType: Optional[ChecksumType]
    MpuObjectSize: Optional[MpuObjectSize]
    RequestPayer: Optional[RequestPayer]
    ExpectedBucketOwner: Optional[AccountId]
    IfMatch: Optional[IfMatch]
    IfNoneMatch: Optional[IfNoneMatch]
    SSECustomerAlgorithm: Optional[SSECustomerAlgorithm]
    SSECustomerKey: Optional[SSECustomerKey]
    SSECustomerKeyMD5: Optional[SSECustomerKeyMD5]


class Condition(TypedDict, total=False):
    HttpErrorCodeReturnedEquals: Optional[HttpErrorCodeReturnedEquals]
    KeyPrefixEquals: Optional[KeyPrefixEquals]


ContentLength = int


class ContinuationEvent(TypedDict, total=False):
    pass


LastModified = datetime


class CopyObjectResult(TypedDict, total=False):
    ETag: Optional[ETag]
    LastModified: Optional[LastModified]
    ChecksumType: Optional[ChecksumType]
    ChecksumCRC32: Optional[ChecksumCRC32]
    ChecksumCRC32C: Optional[ChecksumCRC32C]
    ChecksumCRC64NVME: Optional[ChecksumCRC64NVME]
    ChecksumSHA1: Optional[ChecksumSHA1]
    ChecksumSHA256: Optional[ChecksumSHA256]


class CopyObjectOutput(TypedDict, total=False):
    CopyObjectResult: Optional[CopyObjectResult]
    Expiration: Optional[Expiration]
    CopySourceVersionId: Optional[CopySourceVersionId]
    VersionId: Optional[ObjectVersionId]
    ServerSideEncryption: Optional[ServerSideEncryption]
    SSECustomerAlgorithm: Optional[SSECustomerAlgorithm]
    SSECustomerKeyMD5: Optional[SSECustomerKeyMD5]
    SSEKMSKeyId: Optional[SSEKMSKeyId]
    SSEKMSEncryptionContext: Optional[SSEKMSEncryptionContext]
    BucketKeyEnabled: Optional[BucketKeyEnabled]
    RequestCharged: Optional[RequestCharged]


ObjectLockRetainUntilDate = datetime
Metadata = Dict[MetadataKey, MetadataValue]
CopySourceIfUnmodifiedSince = datetime
CopySourceIfModifiedSince = datetime


class CopyObjectRequest(ServiceRequest):
    ACL: Optional[ObjectCannedACL]
    Bucket: BucketName
    CacheControl: Optional[CacheControl]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    ContentDisposition: Optional[ContentDisposition]
    ContentEncoding: Optional[ContentEncoding]
    ContentLanguage: Optional[ContentLanguage]
    ContentType: Optional[ContentType]
    CopySource: CopySource
    CopySourceIfMatch: Optional[CopySourceIfMatch]
    CopySourceIfModifiedSince: Optional[CopySourceIfModifiedSince]
    CopySourceIfNoneMatch: Optional[CopySourceIfNoneMatch]
    CopySourceIfUnmodifiedSince: Optional[CopySourceIfUnmodifiedSince]
    Expires: Optional[Expires]
    GrantFullControl: Optional[GrantFullControl]
    GrantRead: Optional[GrantRead]
    GrantReadACP: Optional[GrantReadACP]
    GrantWriteACP: Optional[GrantWriteACP]
    Key: ObjectKey
    Metadata: Optional[Metadata]
    MetadataDirective: Optional[MetadataDirective]
    TaggingDirective: Optional[TaggingDirective]
    ServerSideEncryption: Optional[ServerSideEncryption]
    StorageClass: Optional[StorageClass]
    WebsiteRedirectLocation: Optional[WebsiteRedirectLocation]
    SSECustomerAlgorithm: Optional[SSECustomerAlgorithm]
    SSECustomerKey: Optional[SSECustomerKey]
    SSECustomerKeyMD5: Optional[SSECustomerKeyMD5]
    SSEKMSKeyId: Optional[SSEKMSKeyId]
    SSEKMSEncryptionContext: Optional[SSEKMSEncryptionContext]
    BucketKeyEnabled: Optional[BucketKeyEnabled]
    CopySourceSSECustomerAlgorithm: Optional[CopySourceSSECustomerAlgorithm]
    CopySourceSSECustomerKey: Optional[CopySourceSSECustomerKey]
    CopySourceSSECustomerKeyMD5: Optional[CopySourceSSECustomerKeyMD5]
    RequestPayer: Optional[RequestPayer]
    Tagging: Optional[TaggingHeader]
    ObjectLockMode: Optional[ObjectLockMode]
    ObjectLockRetainUntilDate: Optional[ObjectLockRetainUntilDate]
    ObjectLockLegalHoldStatus: Optional[ObjectLockLegalHoldStatus]
    ExpectedBucketOwner: Optional[AccountId]
    ExpectedSourceBucketOwner: Optional[AccountId]


class CopyPartResult(TypedDict, total=False):
    ETag: Optional[ETag]
    LastModified: Optional[LastModified]
    ChecksumCRC32: Optional[ChecksumCRC32]
    ChecksumCRC32C: Optional[ChecksumCRC32C]
    ChecksumCRC64NVME: Optional[ChecksumCRC64NVME]
    ChecksumSHA1: Optional[ChecksumSHA1]
    ChecksumSHA256: Optional[ChecksumSHA256]


class LocationInfo(TypedDict, total=False):
    Type: Optional[LocationType]
    Name: Optional[LocationNameAsString]


class CreateBucketConfiguration(TypedDict, total=False):
    LocationConstraint: Optional[BucketLocationConstraint]
    Location: Optional[LocationInfo]
    Bucket: Optional[BucketInfo]
    Tags: Optional[TagSet]


class MetadataTableEncryptionConfiguration(TypedDict, total=False):
    SseAlgorithm: TableSseAlgorithm
    KmsKeyArn: Optional[KmsKeyArn]


class InventoryTableConfiguration(TypedDict, total=False):
    ConfigurationState: InventoryConfigurationState
    EncryptionConfiguration: Optional[MetadataTableEncryptionConfiguration]


class RecordExpiration(TypedDict, total=False):
    Expiration: ExpirationState
    Days: Optional[RecordExpirationDays]


class JournalTableConfiguration(TypedDict, total=False):
    RecordExpiration: RecordExpiration
    EncryptionConfiguration: Optional[MetadataTableEncryptionConfiguration]


class MetadataConfiguration(TypedDict, total=False):
    JournalTableConfiguration: JournalTableConfiguration
    InventoryTableConfiguration: Optional[InventoryTableConfiguration]


class CreateBucketMetadataConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    ContentMD5: Optional[ContentMD5]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    MetadataConfiguration: MetadataConfiguration
    ExpectedBucketOwner: Optional[AccountId]


class S3TablesDestination(TypedDict, total=False):
    TableBucketArn: S3TablesBucketArn
    TableName: S3TablesName


class MetadataTableConfiguration(TypedDict, total=False):
    S3TablesDestination: S3TablesDestination


class CreateBucketMetadataTableConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    ContentMD5: Optional[ContentMD5]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    MetadataTableConfiguration: MetadataTableConfiguration
    ExpectedBucketOwner: Optional[AccountId]


class CreateBucketOutput(TypedDict, total=False):
    Location: Optional[Location]
    BucketArn: Optional[S3RegionalOrS3ExpressBucketArnString]


class CreateBucketRequest(ServiceRequest):
    ACL: Optional[BucketCannedACL]
    Bucket: BucketName
    CreateBucketConfiguration: Optional[CreateBucketConfiguration]
    GrantFullControl: Optional[GrantFullControl]
    GrantRead: Optional[GrantRead]
    GrantReadACP: Optional[GrantReadACP]
    GrantWrite: Optional[GrantWrite]
    GrantWriteACP: Optional[GrantWriteACP]
    ObjectLockEnabledForBucket: Optional[ObjectLockEnabledForBucket]
    ObjectOwnership: Optional[ObjectOwnership]


class CreateMultipartUploadOutput(TypedDict, total=False):
    AbortDate: Optional[AbortDate]
    AbortRuleId: Optional[AbortRuleId]
    Bucket: Optional[BucketName]
    Key: Optional[ObjectKey]
    UploadId: Optional[MultipartUploadId]
    ServerSideEncryption: Optional[ServerSideEncryption]
    SSECustomerAlgorithm: Optional[SSECustomerAlgorithm]
    SSECustomerKeyMD5: Optional[SSECustomerKeyMD5]
    SSEKMSKeyId: Optional[SSEKMSKeyId]
    SSEKMSEncryptionContext: Optional[SSEKMSEncryptionContext]
    BucketKeyEnabled: Optional[BucketKeyEnabled]
    RequestCharged: Optional[RequestCharged]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    ChecksumType: Optional[ChecksumType]


class CreateMultipartUploadRequest(ServiceRequest):
    ACL: Optional[ObjectCannedACL]
    Bucket: BucketName
    CacheControl: Optional[CacheControl]
    ContentDisposition: Optional[ContentDisposition]
    ContentEncoding: Optional[ContentEncoding]
    ContentLanguage: Optional[ContentLanguage]
    ContentType: Optional[ContentType]
    Expires: Optional[Expires]
    GrantFullControl: Optional[GrantFullControl]
    GrantRead: Optional[GrantRead]
    GrantReadACP: Optional[GrantReadACP]
    GrantWriteACP: Optional[GrantWriteACP]
    Key: ObjectKey
    Metadata: Optional[Metadata]
    ServerSideEncryption: Optional[ServerSideEncryption]
    StorageClass: Optional[StorageClass]
    WebsiteRedirectLocation: Optional[WebsiteRedirectLocation]
    SSECustomerAlgorithm: Optional[SSECustomerAlgorithm]
    SSECustomerKey: Optional[SSECustomerKey]
    SSECustomerKeyMD5: Optional[SSECustomerKeyMD5]
    SSEKMSKeyId: Optional[SSEKMSKeyId]
    SSEKMSEncryptionContext: Optional[SSEKMSEncryptionContext]
    BucketKeyEnabled: Optional[BucketKeyEnabled]
    RequestPayer: Optional[RequestPayer]
    Tagging: Optional[TaggingHeader]
    ObjectLockMode: Optional[ObjectLockMode]
    ObjectLockRetainUntilDate: Optional[ObjectLockRetainUntilDate]
    ObjectLockLegalHoldStatus: Optional[ObjectLockLegalHoldStatus]
    ExpectedBucketOwner: Optional[AccountId]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    ChecksumType: Optional[ChecksumType]


SessionExpiration = datetime


class SessionCredentials(TypedDict, total=False):
    AccessKeyId: AccessKeyIdValue
    SecretAccessKey: SessionCredentialValue
    SessionToken: SessionCredentialValue
    Expiration: SessionExpiration


class CreateSessionOutput(TypedDict, total=False):
    ServerSideEncryption: Optional[ServerSideEncryption]
    SSEKMSKeyId: Optional[SSEKMSKeyId]
    SSEKMSEncryptionContext: Optional[SSEKMSEncryptionContext]
    BucketKeyEnabled: Optional[BucketKeyEnabled]
    Credentials: SessionCredentials


class CreateSessionRequest(ServiceRequest):
    SessionMode: Optional[SessionMode]
    Bucket: BucketName
    ServerSideEncryption: Optional[ServerSideEncryption]
    SSEKMSKeyId: Optional[SSEKMSKeyId]
    SSEKMSEncryptionContext: Optional[SSEKMSEncryptionContext]
    BucketKeyEnabled: Optional[BucketKeyEnabled]


class DefaultRetention(TypedDict, total=False):
    Mode: Optional[ObjectLockRetentionMode]
    Days: Optional[Days]
    Years: Optional[Years]


Size = int
LastModifiedTime = datetime


class ObjectIdentifier(TypedDict, total=False):
    Key: ObjectKey
    VersionId: Optional[ObjectVersionId]
    ETag: Optional[ETag]
    LastModifiedTime: Optional[LastModifiedTime]
    Size: Optional[Size]


ObjectIdentifierList = List[ObjectIdentifier]


class Delete(TypedDict, total=False):
    Objects: ObjectIdentifierList
    Quiet: Optional[Quiet]


class DeleteBucketAnalyticsConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    Id: AnalyticsId
    ExpectedBucketOwner: Optional[AccountId]


class DeleteBucketCorsRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class DeleteBucketEncryptionRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class DeleteBucketIntelligentTieringConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    Id: IntelligentTieringId
    ExpectedBucketOwner: Optional[AccountId]


class DeleteBucketInventoryConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    Id: InventoryId
    ExpectedBucketOwner: Optional[AccountId]


class DeleteBucketLifecycleRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class DeleteBucketMetadataConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class DeleteBucketMetadataTableConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class DeleteBucketMetricsConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    Id: MetricsId
    ExpectedBucketOwner: Optional[AccountId]


class DeleteBucketOwnershipControlsRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class DeleteBucketPolicyRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class DeleteBucketReplicationRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class DeleteBucketRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class DeleteBucketTaggingRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class DeleteBucketWebsiteRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class DeleteMarkerEntry(TypedDict, total=False):
    Owner: Optional[Owner]
    Key: Optional[ObjectKey]
    VersionId: Optional[ObjectVersionId]
    IsLatest: Optional[IsLatest]
    LastModified: Optional[LastModified]


class DeleteMarkerReplication(TypedDict, total=False):
    Status: Optional[DeleteMarkerReplicationStatus]


DeleteMarkers = List[DeleteMarkerEntry]


class DeleteObjectOutput(TypedDict, total=False):
    DeleteMarker: Optional[DeleteMarker]
    VersionId: Optional[ObjectVersionId]
    RequestCharged: Optional[RequestCharged]


IfMatchSize = int
IfMatchLastModifiedTime = datetime


class DeleteObjectRequest(ServiceRequest):
    Bucket: BucketName
    Key: ObjectKey
    MFA: Optional[MFA]
    VersionId: Optional[ObjectVersionId]
    RequestPayer: Optional[RequestPayer]
    BypassGovernanceRetention: Optional[BypassGovernanceRetention]
    ExpectedBucketOwner: Optional[AccountId]
    IfMatch: Optional[IfMatch]
    IfMatchLastModifiedTime: Optional[IfMatchLastModifiedTime]
    IfMatchSize: Optional[IfMatchSize]


class DeleteObjectTaggingOutput(TypedDict, total=False):
    VersionId: Optional[ObjectVersionId]


class DeleteObjectTaggingRequest(ServiceRequest):
    Bucket: BucketName
    Key: ObjectKey
    VersionId: Optional[ObjectVersionId]
    ExpectedBucketOwner: Optional[AccountId]


class Error(TypedDict, total=False):
    Key: Optional[ObjectKey]
    VersionId: Optional[ObjectVersionId]
    Code: Optional[Code]
    Message: Optional[Message]


Errors = List[Error]


class DeletedObject(TypedDict, total=False):
    Key: Optional[ObjectKey]
    VersionId: Optional[ObjectVersionId]
    DeleteMarker: Optional[DeleteMarker]
    DeleteMarkerVersionId: Optional[DeleteMarkerVersionId]


DeletedObjects = List[DeletedObject]


class DeleteObjectsOutput(TypedDict, total=False):
    Deleted: Optional[DeletedObjects]
    RequestCharged: Optional[RequestCharged]
    Errors: Optional[Errors]


class DeleteObjectsRequest(ServiceRequest):
    Bucket: BucketName
    Delete: Delete
    MFA: Optional[MFA]
    RequestPayer: Optional[RequestPayer]
    BypassGovernanceRetention: Optional[BypassGovernanceRetention]
    ExpectedBucketOwner: Optional[AccountId]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]


class DeletePublicAccessBlockRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class ReplicationTimeValue(TypedDict, total=False):
    Minutes: Optional[Minutes]


class Metrics(TypedDict, total=False):
    Status: MetricsStatus
    EventThreshold: Optional[ReplicationTimeValue]


class ReplicationTime(TypedDict, total=False):
    Status: ReplicationTimeStatus
    Time: ReplicationTimeValue


class EncryptionConfiguration(TypedDict, total=False):
    ReplicaKmsKeyID: Optional[ReplicaKmsKeyID]


class Destination(TypedDict, total=False):
    Bucket: BucketName
    Account: Optional[AccountId]
    StorageClass: Optional[StorageClass]
    AccessControlTranslation: Optional[AccessControlTranslation]
    EncryptionConfiguration: Optional[EncryptionConfiguration]
    ReplicationTime: Optional[ReplicationTime]
    Metrics: Optional[Metrics]


class DestinationResult(TypedDict, total=False):
    TableBucketType: Optional[S3TablesBucketType]
    TableBucketArn: Optional[S3TablesBucketArn]
    TableNamespace: Optional[S3TablesNamespace]


class Encryption(TypedDict, total=False):
    EncryptionType: ServerSideEncryption
    KMSKeyId: Optional[SSEKMSKeyId]
    KMSContext: Optional[KMSContext]


End = int


class EndEvent(TypedDict, total=False):
    pass


class ErrorDetails(TypedDict, total=False):
    ErrorCode: Optional[ErrorCode]
    ErrorMessage: Optional[ErrorMessage]


class ErrorDocument(TypedDict, total=False):
    Key: ObjectKey


class EventBridgeConfiguration(TypedDict, total=False):
    pass


class ExistingObjectReplication(TypedDict, total=False):
    Status: ExistingObjectReplicationStatus


class FilterRule(TypedDict, total=False):
    Name: Optional[FilterRuleName]
    Value: Optional[FilterRuleValue]


FilterRuleList = List[FilterRule]


class GetBucketAccelerateConfigurationOutput(TypedDict, total=False):
    Status: Optional[BucketAccelerateStatus]
    RequestCharged: Optional[RequestCharged]


class GetBucketAccelerateConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]
    RequestPayer: Optional[RequestPayer]


class GetBucketAclOutput(TypedDict, total=False):
    Owner: Optional[Owner]
    Grants: Optional[Grants]


class GetBucketAclRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class GetBucketAnalyticsConfigurationOutput(TypedDict, total=False):
    AnalyticsConfiguration: Optional[AnalyticsConfiguration]


class GetBucketAnalyticsConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    Id: AnalyticsId
    ExpectedBucketOwner: Optional[AccountId]


class GetBucketCorsOutput(TypedDict, total=False):
    CORSRules: Optional[CORSRules]


class GetBucketCorsRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class ServerSideEncryptionByDefault(TypedDict, total=False):
    SSEAlgorithm: ServerSideEncryption
    KMSMasterKeyID: Optional[SSEKMSKeyId]


class ServerSideEncryptionRule(TypedDict, total=False):
    ApplyServerSideEncryptionByDefault: Optional[ServerSideEncryptionByDefault]
    BucketKeyEnabled: Optional[BucketKeyEnabled]


ServerSideEncryptionRules = List[ServerSideEncryptionRule]


class ServerSideEncryptionConfiguration(TypedDict, total=False):
    Rules: ServerSideEncryptionRules


class GetBucketEncryptionOutput(TypedDict, total=False):
    ServerSideEncryptionConfiguration: Optional[ServerSideEncryptionConfiguration]


class GetBucketEncryptionRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class Tiering(TypedDict, total=False):
    Days: IntelligentTieringDays
    AccessTier: IntelligentTieringAccessTier


TieringList = List[Tiering]


class IntelligentTieringAndOperator(TypedDict, total=False):
    Prefix: Optional[Prefix]
    Tags: Optional[TagSet]


class IntelligentTieringFilter(TypedDict, total=False):
    Prefix: Optional[Prefix]
    Tag: Optional[Tag]
    And: Optional[IntelligentTieringAndOperator]


class IntelligentTieringConfiguration(TypedDict, total=False):
    Id: IntelligentTieringId
    Filter: Optional[IntelligentTieringFilter]
    Status: IntelligentTieringStatus
    Tierings: TieringList


class GetBucketIntelligentTieringConfigurationOutput(TypedDict, total=False):
    IntelligentTieringConfiguration: Optional[IntelligentTieringConfiguration]


class GetBucketIntelligentTieringConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    Id: IntelligentTieringId
    ExpectedBucketOwner: Optional[AccountId]


class InventorySchedule(TypedDict, total=False):
    Frequency: InventoryFrequency


InventoryOptionalFields = List[InventoryOptionalField]


class InventoryFilter(TypedDict, total=False):
    Prefix: Prefix


class SSEKMS(TypedDict, total=False):
    KeyId: SSEKMSKeyId


class SSES3(TypedDict, total=False):
    pass


class InventoryEncryption(TypedDict, total=False):
    SSES3: Optional[SSES3]
    SSEKMS: Optional[SSEKMS]


class InventoryS3BucketDestination(TypedDict, total=False):
    AccountId: Optional[AccountId]
    Bucket: BucketName
    Format: InventoryFormat
    Prefix: Optional[Prefix]
    Encryption: Optional[InventoryEncryption]


class InventoryDestination(TypedDict, total=False):
    S3BucketDestination: InventoryS3BucketDestination


class InventoryConfiguration(TypedDict, total=False):
    Destination: InventoryDestination
    IsEnabled: IsEnabled
    Filter: Optional[InventoryFilter]
    Id: InventoryId
    IncludedObjectVersions: InventoryIncludedObjectVersions
    OptionalFields: Optional[InventoryOptionalFields]
    Schedule: InventorySchedule


class GetBucketInventoryConfigurationOutput(TypedDict, total=False):
    InventoryConfiguration: Optional[InventoryConfiguration]


class GetBucketInventoryConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    Id: InventoryId
    ExpectedBucketOwner: Optional[AccountId]


class GetBucketLifecycleConfigurationOutput(TypedDict, total=False):
    Rules: Optional[LifecycleRules]
    TransitionDefaultMinimumObjectSize: Optional[TransitionDefaultMinimumObjectSize]


class GetBucketLifecycleConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class Rule(TypedDict, total=False):
    Expiration: Optional[LifecycleExpiration]
    ID: Optional[ID]
    Prefix: Prefix
    Status: ExpirationStatus
    Transition: Optional[Transition]
    NoncurrentVersionTransition: Optional[NoncurrentVersionTransition]
    NoncurrentVersionExpiration: Optional[NoncurrentVersionExpiration]
    AbortIncompleteMultipartUpload: Optional[AbortIncompleteMultipartUpload]


Rules = List[Rule]


class GetBucketLifecycleOutput(TypedDict, total=False):
    Rules: Optional[Rules]


class GetBucketLifecycleRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class GetBucketLocationOutput(TypedDict, total=False):
    LocationConstraint: Optional[BucketLocationConstraint]


class GetBucketLocationRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class GetBucketLoggingOutput(TypedDict, total=False):
    LoggingEnabled: Optional[LoggingEnabled]


class GetBucketLoggingRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class InventoryTableConfigurationResult(TypedDict, total=False):
    ConfigurationState: InventoryConfigurationState
    TableStatus: Optional[MetadataTableStatus]
    Error: Optional[ErrorDetails]
    TableName: Optional[S3TablesName]
    TableArn: Optional[S3TablesArn]


class JournalTableConfigurationResult(TypedDict, total=False):
    TableStatus: MetadataTableStatus
    Error: Optional[ErrorDetails]
    TableName: S3TablesName
    TableArn: Optional[S3TablesArn]
    RecordExpiration: RecordExpiration


class MetadataConfigurationResult(TypedDict, total=False):
    DestinationResult: DestinationResult
    JournalTableConfigurationResult: Optional[JournalTableConfigurationResult]
    InventoryTableConfigurationResult: Optional[InventoryTableConfigurationResult]


class GetBucketMetadataConfigurationResult(TypedDict, total=False):
    MetadataConfigurationResult: MetadataConfigurationResult


class GetBucketMetadataConfigurationOutput(TypedDict, total=False):
    GetBucketMetadataConfigurationResult: Optional[GetBucketMetadataConfigurationResult]


class GetBucketMetadataConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class S3TablesDestinationResult(TypedDict, total=False):
    TableBucketArn: S3TablesBucketArn
    TableName: S3TablesName
    TableArn: S3TablesArn
    TableNamespace: S3TablesNamespace


class MetadataTableConfigurationResult(TypedDict, total=False):
    S3TablesDestinationResult: S3TablesDestinationResult


class GetBucketMetadataTableConfigurationResult(TypedDict, total=False):
    MetadataTableConfigurationResult: MetadataTableConfigurationResult
    Status: MetadataTableStatus
    Error: Optional[ErrorDetails]


class GetBucketMetadataTableConfigurationOutput(TypedDict, total=False):
    GetBucketMetadataTableConfigurationResult: Optional[GetBucketMetadataTableConfigurationResult]


class GetBucketMetadataTableConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class MetricsAndOperator(TypedDict, total=False):
    Prefix: Optional[Prefix]
    Tags: Optional[TagSet]
    AccessPointArn: Optional[AccessPointArn]


class MetricsFilter(TypedDict, total=False):
    Prefix: Optional[Prefix]
    Tag: Optional[Tag]
    AccessPointArn: Optional[AccessPointArn]
    And: Optional[MetricsAndOperator]


class MetricsConfiguration(TypedDict, total=False):
    Id: MetricsId
    Filter: Optional[MetricsFilter]


class GetBucketMetricsConfigurationOutput(TypedDict, total=False):
    MetricsConfiguration: Optional[MetricsConfiguration]


class GetBucketMetricsConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    Id: MetricsId
    ExpectedBucketOwner: Optional[AccountId]


class GetBucketNotificationConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class OwnershipControlsRule(TypedDict, total=False):
    ObjectOwnership: ObjectOwnership


OwnershipControlsRules = List[OwnershipControlsRule]


class OwnershipControls(TypedDict, total=False):
    Rules: OwnershipControlsRules


class GetBucketOwnershipControlsOutput(TypedDict, total=False):
    OwnershipControls: Optional[OwnershipControls]


class GetBucketOwnershipControlsRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class GetBucketPolicyOutput(TypedDict, total=False):
    Policy: Optional[Policy]


class GetBucketPolicyRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class PolicyStatus(TypedDict, total=False):
    IsPublic: Optional[IsPublic]


class GetBucketPolicyStatusOutput(TypedDict, total=False):
    PolicyStatus: Optional[PolicyStatus]


class GetBucketPolicyStatusRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class ReplicaModifications(TypedDict, total=False):
    Status: ReplicaModificationsStatus


class SseKmsEncryptedObjects(TypedDict, total=False):
    Status: SseKmsEncryptedObjectsStatus


class SourceSelectionCriteria(TypedDict, total=False):
    SseKmsEncryptedObjects: Optional[SseKmsEncryptedObjects]
    ReplicaModifications: Optional[ReplicaModifications]


class ReplicationRuleAndOperator(TypedDict, total=False):
    Prefix: Optional[Prefix]
    Tags: Optional[TagSet]


class ReplicationRuleFilter(TypedDict, total=False):
    Prefix: Optional[Prefix]
    Tag: Optional[Tag]
    And: Optional[ReplicationRuleAndOperator]


class ReplicationRule(TypedDict, total=False):
    ID: Optional[ID]
    Priority: Optional[Priority]
    Prefix: Optional[Prefix]
    Filter: Optional[ReplicationRuleFilter]
    Status: ReplicationRuleStatus
    SourceSelectionCriteria: Optional[SourceSelectionCriteria]
    ExistingObjectReplication: Optional[ExistingObjectReplication]
    Destination: Destination
    DeleteMarkerReplication: Optional[DeleteMarkerReplication]


ReplicationRules = List[ReplicationRule]


class ReplicationConfiguration(TypedDict, total=False):
    Role: Role
    Rules: ReplicationRules


class GetBucketReplicationOutput(TypedDict, total=False):
    ReplicationConfiguration: Optional[ReplicationConfiguration]


class GetBucketReplicationRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class GetBucketRequestPaymentOutput(TypedDict, total=False):
    Payer: Optional[Payer]


class GetBucketRequestPaymentRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class GetBucketTaggingOutput(TypedDict, total=False):
    TagSet: TagSet


class GetBucketTaggingRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class GetBucketVersioningOutput(TypedDict, total=False):
    Status: Optional[BucketVersioningStatus]
    MFADelete: Optional[MFADeleteStatus]


class GetBucketVersioningRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class Redirect(TypedDict, total=False):
    HostName: Optional[HostName]
    HttpRedirectCode: Optional[HttpRedirectCode]
    Protocol: Optional[Protocol]
    ReplaceKeyPrefixWith: Optional[ReplaceKeyPrefixWith]
    ReplaceKeyWith: Optional[ReplaceKeyWith]


class RoutingRule(TypedDict, total=False):
    Condition: Optional[Condition]
    Redirect: Redirect


RoutingRules = List[RoutingRule]


class IndexDocument(TypedDict, total=False):
    Suffix: Suffix


class RedirectAllRequestsTo(TypedDict, total=False):
    HostName: HostName
    Protocol: Optional[Protocol]


class GetBucketWebsiteOutput(TypedDict, total=False):
    RedirectAllRequestsTo: Optional[RedirectAllRequestsTo]
    IndexDocument: Optional[IndexDocument]
    ErrorDocument: Optional[ErrorDocument]
    RoutingRules: Optional[RoutingRules]


class GetBucketWebsiteRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class GetObjectAclOutput(TypedDict, total=False):
    Owner: Optional[Owner]
    Grants: Optional[Grants]
    RequestCharged: Optional[RequestCharged]


class GetObjectAclRequest(ServiceRequest):
    Bucket: BucketName
    Key: ObjectKey
    VersionId: Optional[ObjectVersionId]
    RequestPayer: Optional[RequestPayer]
    ExpectedBucketOwner: Optional[AccountId]


class ObjectPart(TypedDict, total=False):
    PartNumber: Optional[PartNumber]
    Size: Optional[Size]
    ChecksumCRC32: Optional[ChecksumCRC32]
    ChecksumCRC32C: Optional[ChecksumCRC32C]
    ChecksumCRC64NVME: Optional[ChecksumCRC64NVME]
    ChecksumSHA1: Optional[ChecksumSHA1]
    ChecksumSHA256: Optional[ChecksumSHA256]


PartsList = List[ObjectPart]


class GetObjectAttributesParts(TypedDict, total=False):
    TotalPartsCount: Optional[PartsCount]
    PartNumberMarker: Optional[PartNumberMarker]
    NextPartNumberMarker: Optional[NextPartNumberMarker]
    MaxParts: Optional[MaxParts]
    IsTruncated: Optional[IsTruncated]
    Parts: Optional[PartsList]


class GetObjectAttributesOutput(TypedDict, total=False):
    DeleteMarker: Optional[DeleteMarker]
    LastModified: Optional[LastModified]
    VersionId: Optional[ObjectVersionId]
    RequestCharged: Optional[RequestCharged]
    ETag: Optional[ETag]
    Checksum: Optional[Checksum]
    ObjectParts: Optional[GetObjectAttributesParts]
    StorageClass: Optional[StorageClass]
    ObjectSize: Optional[ObjectSize]


ObjectAttributesList = List[ObjectAttributes]


class GetObjectAttributesRequest(ServiceRequest):
    Bucket: BucketName
    Key: ObjectKey
    VersionId: Optional[ObjectVersionId]
    MaxParts: Optional[MaxParts]
    PartNumberMarker: Optional[PartNumberMarker]
    SSECustomerAlgorithm: Optional[SSECustomerAlgorithm]
    SSECustomerKey: Optional[SSECustomerKey]
    SSECustomerKeyMD5: Optional[SSECustomerKeyMD5]
    RequestPayer: Optional[RequestPayer]
    ExpectedBucketOwner: Optional[AccountId]
    ObjectAttributes: ObjectAttributesList


class ObjectLockLegalHold(TypedDict, total=False):
    Status: Optional[ObjectLockLegalHoldStatus]


class GetObjectLegalHoldOutput(TypedDict, total=False):
    LegalHold: Optional[ObjectLockLegalHold]


class GetObjectLegalHoldRequest(ServiceRequest):
    Bucket: BucketName
    Key: ObjectKey
    VersionId: Optional[ObjectVersionId]
    RequestPayer: Optional[RequestPayer]
    ExpectedBucketOwner: Optional[AccountId]


class ObjectLockRule(TypedDict, total=False):
    DefaultRetention: Optional[DefaultRetention]


class ObjectLockConfiguration(TypedDict, total=False):
    ObjectLockEnabled: Optional[ObjectLockEnabled]
    Rule: Optional[ObjectLockRule]


class GetObjectLockConfigurationOutput(TypedDict, total=False):
    ObjectLockConfiguration: Optional[ObjectLockConfiguration]


class GetObjectLockConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class GetObjectOutput(TypedDict, total=False):
    Body: Optional[Union[Body, IO[Body], Iterable[Body]]]
    DeleteMarker: Optional[DeleteMarker]
    AcceptRanges: Optional[AcceptRanges]
    Expiration: Optional[Expiration]
    Restore: Optional[Restore]
    LastModified: Optional[LastModified]
    ContentLength: Optional[ContentLength]
    ETag: Optional[ETag]
    ChecksumCRC32: Optional[ChecksumCRC32]
    ChecksumCRC32C: Optional[ChecksumCRC32C]
    ChecksumCRC64NVME: Optional[ChecksumCRC64NVME]
    ChecksumSHA1: Optional[ChecksumSHA1]
    ChecksumSHA256: Optional[ChecksumSHA256]
    ChecksumType: Optional[ChecksumType]
    MissingMeta: Optional[MissingMeta]
    VersionId: Optional[ObjectVersionId]
    CacheControl: Optional[CacheControl]
    ContentDisposition: Optional[ContentDisposition]
    ContentEncoding: Optional[ContentEncoding]
    ContentLanguage: Optional[ContentLanguage]
    ContentRange: Optional[ContentRange]
    ContentType: Optional[ContentType]
    Expires: Optional[Expires]
    WebsiteRedirectLocation: Optional[WebsiteRedirectLocation]
    ServerSideEncryption: Optional[ServerSideEncryption]
    Metadata: Optional[Metadata]
    SSECustomerAlgorithm: Optional[SSECustomerAlgorithm]
    SSECustomerKeyMD5: Optional[SSECustomerKeyMD5]
    SSEKMSKeyId: Optional[SSEKMSKeyId]
    BucketKeyEnabled: Optional[BucketKeyEnabled]
    StorageClass: Optional[StorageClass]
    RequestCharged: Optional[RequestCharged]
    ReplicationStatus: Optional[ReplicationStatus]
    PartsCount: Optional[PartsCount]
    TagCount: Optional[TagCount]
    ObjectLockMode: Optional[ObjectLockMode]
    ObjectLockRetainUntilDate: Optional[ObjectLockRetainUntilDate]
    ObjectLockLegalHoldStatus: Optional[ObjectLockLegalHoldStatus]
    StatusCode: Optional[GetObjectResponseStatusCode]


ResponseExpires = datetime
IfUnmodifiedSince = datetime
IfModifiedSince = datetime


class GetObjectRequest(ServiceRequest):
    Bucket: BucketName
    IfMatch: Optional[IfMatch]
    IfModifiedSince: Optional[IfModifiedSince]
    IfNoneMatch: Optional[IfNoneMatch]
    IfUnmodifiedSince: Optional[IfUnmodifiedSince]
    Key: ObjectKey
    Range: Optional[Range]
    ResponseCacheControl: Optional[ResponseCacheControl]
    ResponseContentDisposition: Optional[ResponseContentDisposition]
    ResponseContentEncoding: Optional[ResponseContentEncoding]
    ResponseContentLanguage: Optional[ResponseContentLanguage]
    ResponseContentType: Optional[ResponseContentType]
    ResponseExpires: Optional[ResponseExpires]
    VersionId: Optional[ObjectVersionId]
    SSECustomerAlgorithm: Optional[SSECustomerAlgorithm]
    SSECustomerKey: Optional[SSECustomerKey]
    SSECustomerKeyMD5: Optional[SSECustomerKeyMD5]
    RequestPayer: Optional[RequestPayer]
    PartNumber: Optional[PartNumber]
    ExpectedBucketOwner: Optional[AccountId]
    ChecksumMode: Optional[ChecksumMode]


class ObjectLockRetention(TypedDict, total=False):
    Mode: Optional[ObjectLockRetentionMode]
    RetainUntilDate: Optional[Date]


class GetObjectRetentionOutput(TypedDict, total=False):
    Retention: Optional[ObjectLockRetention]


class GetObjectRetentionRequest(ServiceRequest):
    Bucket: BucketName
    Key: ObjectKey
    VersionId: Optional[ObjectVersionId]
    RequestPayer: Optional[RequestPayer]
    ExpectedBucketOwner: Optional[AccountId]


class GetObjectTaggingOutput(TypedDict, total=False):
    VersionId: Optional[ObjectVersionId]
    TagSet: TagSet


class GetObjectTaggingRequest(ServiceRequest):
    Bucket: BucketName
    Key: ObjectKey
    VersionId: Optional[ObjectVersionId]
    ExpectedBucketOwner: Optional[AccountId]
    RequestPayer: Optional[RequestPayer]


class GetObjectTorrentOutput(TypedDict, total=False):
    Body: Optional[Union[Body, IO[Body], Iterable[Body]]]
    RequestCharged: Optional[RequestCharged]


class GetObjectTorrentRequest(ServiceRequest):
    Bucket: BucketName
    Key: ObjectKey
    RequestPayer: Optional[RequestPayer]
    ExpectedBucketOwner: Optional[AccountId]


class PublicAccessBlockConfiguration(TypedDict, total=False):
    BlockPublicAcls: Optional[Setting]
    IgnorePublicAcls: Optional[Setting]
    BlockPublicPolicy: Optional[Setting]
    RestrictPublicBuckets: Optional[Setting]


class GetPublicAccessBlockOutput(TypedDict, total=False):
    PublicAccessBlockConfiguration: Optional[PublicAccessBlockConfiguration]


class GetPublicAccessBlockRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class GlacierJobParameters(TypedDict, total=False):
    Tier: Tier


class HeadBucketOutput(TypedDict, total=False):
    BucketRegion: Optional[BucketRegion]
    BucketContentType: Optional[BucketContentType]


class HeadBucketRequest(ServiceRequest):
    Bucket: BucketName
    ExpectedBucketOwner: Optional[AccountId]


class HeadObjectOutput(TypedDict, total=False):
    DeleteMarker: Optional[DeleteMarker]
    AcceptRanges: Optional[AcceptRanges]
    Expiration: Optional[Expiration]
    Restore: Optional[Restore]
    ArchiveStatus: Optional[ArchiveStatus]
    LastModified: Optional[LastModified]
    ContentLength: Optional[ContentLength]
    ChecksumCRC32: Optional[ChecksumCRC32]
    ChecksumCRC32C: Optional[ChecksumCRC32C]
    ChecksumCRC64NVME: Optional[ChecksumCRC64NVME]
    ChecksumSHA1: Optional[ChecksumSHA1]
    ChecksumSHA256: Optional[ChecksumSHA256]
    ChecksumType: Optional[ChecksumType]
    ETag: Optional[ETag]
    MissingMeta: Optional[MissingMeta]
    VersionId: Optional[ObjectVersionId]
    CacheControl: Optional[CacheControl]
    ContentDisposition: Optional[ContentDisposition]
    ContentEncoding: Optional[ContentEncoding]
    ContentLanguage: Optional[ContentLanguage]
    ContentType: Optional[ContentType]
    ContentRange: Optional[ContentRange]
    Expires: Optional[Expires]
    WebsiteRedirectLocation: Optional[WebsiteRedirectLocation]
    ServerSideEncryption: Optional[ServerSideEncryption]
    Metadata: Optional[Metadata]
    SSECustomerAlgorithm: Optional[SSECustomerAlgorithm]
    SSECustomerKeyMD5: Optional[SSECustomerKeyMD5]
    SSEKMSKeyId: Optional[SSEKMSKeyId]
    BucketKeyEnabled: Optional[BucketKeyEnabled]
    StorageClass: Optional[StorageClass]
    RequestCharged: Optional[RequestCharged]
    ReplicationStatus: Optional[ReplicationStatus]
    PartsCount: Optional[PartsCount]
    TagCount: Optional[TagCount]
    ObjectLockMode: Optional[ObjectLockMode]
    ObjectLockRetainUntilDate: Optional[ObjectLockRetainUntilDate]
    ObjectLockLegalHoldStatus: Optional[ObjectLockLegalHoldStatus]
    StatusCode: Optional[GetObjectResponseStatusCode]


class HeadObjectRequest(ServiceRequest):
    Bucket: BucketName
    IfMatch: Optional[IfMatch]
    IfModifiedSince: Optional[IfModifiedSince]
    IfNoneMatch: Optional[IfNoneMatch]
    IfUnmodifiedSince: Optional[IfUnmodifiedSince]
    Key: ObjectKey
    Range: Optional[Range]
    ResponseCacheControl: Optional[ResponseCacheControl]
    ResponseContentDisposition: Optional[ResponseContentDisposition]
    ResponseContentEncoding: Optional[ResponseContentEncoding]
    ResponseContentLanguage: Optional[ResponseContentLanguage]
    ResponseContentType: Optional[ResponseContentType]
    ResponseExpires: Optional[ResponseExpires]
    VersionId: Optional[ObjectVersionId]
    SSECustomerAlgorithm: Optional[SSECustomerAlgorithm]
    SSECustomerKey: Optional[SSECustomerKey]
    SSECustomerKeyMD5: Optional[SSECustomerKeyMD5]
    RequestPayer: Optional[RequestPayer]
    PartNumber: Optional[PartNumber]
    ExpectedBucketOwner: Optional[AccountId]
    ChecksumMode: Optional[ChecksumMode]


Initiated = datetime


class Initiator(TypedDict, total=False):
    ID: Optional[ID]
    DisplayName: Optional[DisplayName]


class ParquetInput(TypedDict, total=False):
    pass


class JSONInput(TypedDict, total=False):
    Type: Optional[JSONType]


class InputSerialization(TypedDict, total=False):
    CSV: Optional[CSVInput]
    CompressionType: Optional[CompressionType]
    JSON: Optional[JSONInput]
    Parquet: Optional[ParquetInput]


IntelligentTieringConfigurationList = List[IntelligentTieringConfiguration]
InventoryConfigurationList = List[InventoryConfiguration]


class InventoryTableConfigurationUpdates(TypedDict, total=False):
    ConfigurationState: InventoryConfigurationState
    EncryptionConfiguration: Optional[MetadataTableEncryptionConfiguration]


class JSONOutput(TypedDict, total=False):
    RecordDelimiter: Optional[RecordDelimiter]


class JournalTableConfigurationUpdates(TypedDict, total=False):
    RecordExpiration: RecordExpiration


class S3KeyFilter(TypedDict, total=False):
    FilterRules: Optional[FilterRuleList]


class NotificationConfigurationFilter(TypedDict, total=False):
    Key: Optional[S3KeyFilter]


class LambdaFunctionConfiguration(TypedDict, total=False):
    Id: Optional[NotificationId]
    LambdaFunctionArn: LambdaFunctionArn
    Events: EventList
    Filter: Optional[NotificationConfigurationFilter]


LambdaFunctionConfigurationList = List[LambdaFunctionConfiguration]


class LifecycleConfiguration(TypedDict, total=False):
    Rules: Rules


class ListBucketAnalyticsConfigurationsOutput(TypedDict, total=False):
    IsTruncated: Optional[IsTruncated]
    ContinuationToken: Optional[Token]
    NextContinuationToken: Optional[NextToken]
    AnalyticsConfigurationList: Optional[AnalyticsConfigurationList]


class ListBucketAnalyticsConfigurationsRequest(ServiceRequest):
    Bucket: BucketName
    ContinuationToken: Optional[Token]
    ExpectedBucketOwner: Optional[AccountId]


class ListBucketIntelligentTieringConfigurationsOutput(TypedDict, total=False):
    IsTruncated: Optional[IsTruncated]
    ContinuationToken: Optional[Token]
    NextContinuationToken: Optional[NextToken]
    IntelligentTieringConfigurationList: Optional[IntelligentTieringConfigurationList]


class ListBucketIntelligentTieringConfigurationsRequest(ServiceRequest):
    Bucket: BucketName
    ContinuationToken: Optional[Token]
    ExpectedBucketOwner: Optional[AccountId]


class ListBucketInventoryConfigurationsOutput(TypedDict, total=False):
    ContinuationToken: Optional[Token]
    InventoryConfigurationList: Optional[InventoryConfigurationList]
    IsTruncated: Optional[IsTruncated]
    NextContinuationToken: Optional[NextToken]


class ListBucketInventoryConfigurationsRequest(ServiceRequest):
    Bucket: BucketName
    ContinuationToken: Optional[Token]
    ExpectedBucketOwner: Optional[AccountId]


MetricsConfigurationList = List[MetricsConfiguration]


class ListBucketMetricsConfigurationsOutput(TypedDict, total=False):
    IsTruncated: Optional[IsTruncated]
    ContinuationToken: Optional[Token]
    NextContinuationToken: Optional[NextToken]
    MetricsConfigurationList: Optional[MetricsConfigurationList]


class ListBucketMetricsConfigurationsRequest(ServiceRequest):
    Bucket: BucketName
    ContinuationToken: Optional[Token]
    ExpectedBucketOwner: Optional[AccountId]


class ListBucketsOutput(TypedDict, total=False):
    Owner: Optional[Owner]
    ContinuationToken: Optional[NextToken]
    Prefix: Optional[Prefix]
    Buckets: Optional[Buckets]


class ListBucketsRequest(ServiceRequest):
    MaxBuckets: Optional[MaxBuckets]
    ContinuationToken: Optional[Token]
    Prefix: Optional[Prefix]
    BucketRegion: Optional[BucketRegion]


class ListDirectoryBucketsOutput(TypedDict, total=False):
    Buckets: Optional[Buckets]
    ContinuationToken: Optional[DirectoryBucketToken]


class ListDirectoryBucketsRequest(ServiceRequest):
    ContinuationToken: Optional[DirectoryBucketToken]
    MaxDirectoryBuckets: Optional[MaxDirectoryBuckets]


class MultipartUpload(TypedDict, total=False):
    UploadId: Optional[MultipartUploadId]
    Key: Optional[ObjectKey]
    Initiated: Optional[Initiated]
    StorageClass: Optional[StorageClass]
    Owner: Optional[Owner]
    Initiator: Optional[Initiator]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    ChecksumType: Optional[ChecksumType]


MultipartUploadList = List[MultipartUpload]


class ListMultipartUploadsOutput(TypedDict, total=False):
    Bucket: Optional[BucketName]
    KeyMarker: Optional[KeyMarker]
    UploadIdMarker: Optional[UploadIdMarker]
    NextKeyMarker: Optional[NextKeyMarker]
    Prefix: Optional[Prefix]
    Delimiter: Optional[Delimiter]
    NextUploadIdMarker: Optional[NextUploadIdMarker]
    MaxUploads: Optional[MaxUploads]
    IsTruncated: Optional[IsTruncated]
    Uploads: Optional[MultipartUploadList]
    CommonPrefixes: Optional[CommonPrefixList]
    EncodingType: Optional[EncodingType]
    RequestCharged: Optional[RequestCharged]


class ListMultipartUploadsRequest(ServiceRequest):
    Bucket: BucketName
    Delimiter: Optional[Delimiter]
    EncodingType: Optional[EncodingType]
    KeyMarker: Optional[KeyMarker]
    MaxUploads: Optional[MaxUploads]
    Prefix: Optional[Prefix]
    UploadIdMarker: Optional[UploadIdMarker]
    ExpectedBucketOwner: Optional[AccountId]
    RequestPayer: Optional[RequestPayer]


RestoreExpiryDate = datetime


class RestoreStatus(TypedDict, total=False):
    IsRestoreInProgress: Optional[IsRestoreInProgress]
    RestoreExpiryDate: Optional[RestoreExpiryDate]


class ObjectVersion(TypedDict, total=False):
    ETag: Optional[ETag]
    ChecksumAlgorithm: Optional[ChecksumAlgorithmList]
    ChecksumType: Optional[ChecksumType]
    Size: Optional[Size]
    StorageClass: Optional[ObjectVersionStorageClass]
    Key: Optional[ObjectKey]
    VersionId: Optional[ObjectVersionId]
    IsLatest: Optional[IsLatest]
    LastModified: Optional[LastModified]
    Owner: Optional[Owner]
    RestoreStatus: Optional[RestoreStatus]


ObjectVersionList = List[ObjectVersion]


class ListObjectVersionsOutput(TypedDict, total=False):
    IsTruncated: Optional[IsTruncated]
    KeyMarker: Optional[KeyMarker]
    VersionIdMarker: Optional[VersionIdMarker]
    NextKeyMarker: Optional[NextKeyMarker]
    NextVersionIdMarker: Optional[NextVersionIdMarker]
    DeleteMarkers: Optional[DeleteMarkers]
    Name: Optional[BucketName]
    Prefix: Optional[Prefix]
    Delimiter: Optional[Delimiter]
    MaxKeys: Optional[MaxKeys]
    CommonPrefixes: Optional[CommonPrefixList]
    EncodingType: Optional[EncodingType]
    RequestCharged: Optional[RequestCharged]
    Versions: Optional[ObjectVersionList]


OptionalObjectAttributesList = List[OptionalObjectAttributes]


class ListObjectVersionsRequest(ServiceRequest):
    Bucket: BucketName
    Delimiter: Optional[Delimiter]
    EncodingType: Optional[EncodingType]
    KeyMarker: Optional[KeyMarker]
    MaxKeys: Optional[MaxKeys]
    Prefix: Optional[Prefix]
    VersionIdMarker: Optional[VersionIdMarker]
    ExpectedBucketOwner: Optional[AccountId]
    RequestPayer: Optional[RequestPayer]
    OptionalObjectAttributes: Optional[OptionalObjectAttributesList]


class Object(TypedDict, total=False):
    Key: Optional[ObjectKey]
    LastModified: Optional[LastModified]
    ETag: Optional[ETag]
    ChecksumAlgorithm: Optional[ChecksumAlgorithmList]
    ChecksumType: Optional[ChecksumType]
    Size: Optional[Size]
    StorageClass: Optional[ObjectStorageClass]
    Owner: Optional[Owner]
    RestoreStatus: Optional[RestoreStatus]


ObjectList = List[Object]


class ListObjectsOutput(TypedDict, total=False):
    IsTruncated: Optional[IsTruncated]
    Marker: Optional[Marker]
    NextMarker: Optional[NextMarker]
    Name: Optional[BucketName]
    Prefix: Optional[Prefix]
    Delimiter: Optional[Delimiter]
    MaxKeys: Optional[MaxKeys]
    CommonPrefixes: Optional[CommonPrefixList]
    EncodingType: Optional[EncodingType]
    RequestCharged: Optional[RequestCharged]
    BucketRegion: Optional[BucketRegion]
    Contents: Optional[ObjectList]


class ListObjectsRequest(ServiceRequest):
    Bucket: BucketName
    Delimiter: Optional[Delimiter]
    EncodingType: Optional[EncodingType]
    Marker: Optional[Marker]
    MaxKeys: Optional[MaxKeys]
    Prefix: Optional[Prefix]
    RequestPayer: Optional[RequestPayer]
    ExpectedBucketOwner: Optional[AccountId]
    OptionalObjectAttributes: Optional[OptionalObjectAttributesList]


class ListObjectsV2Output(TypedDict, total=False):
    IsTruncated: Optional[IsTruncated]
    Name: Optional[BucketName]
    Prefix: Optional[Prefix]
    Delimiter: Optional[Delimiter]
    MaxKeys: Optional[MaxKeys]
    CommonPrefixes: Optional[CommonPrefixList]
    EncodingType: Optional[EncodingType]
    KeyCount: Optional[KeyCount]
    ContinuationToken: Optional[Token]
    NextContinuationToken: Optional[NextToken]
    StartAfter: Optional[StartAfter]
    RequestCharged: Optional[RequestCharged]
    BucketRegion: Optional[BucketRegion]
    Contents: Optional[ObjectList]


class ListObjectsV2Request(ServiceRequest):
    Bucket: BucketName
    Delimiter: Optional[Delimiter]
    EncodingType: Optional[EncodingType]
    MaxKeys: Optional[MaxKeys]
    Prefix: Optional[Prefix]
    ContinuationToken: Optional[Token]
    FetchOwner: Optional[FetchOwner]
    StartAfter: Optional[StartAfter]
    RequestPayer: Optional[RequestPayer]
    ExpectedBucketOwner: Optional[AccountId]
    OptionalObjectAttributes: Optional[OptionalObjectAttributesList]


class Part(TypedDict, total=False):
    PartNumber: Optional[PartNumber]
    LastModified: Optional[LastModified]
    ETag: Optional[ETag]
    Size: Optional[Size]
    ChecksumCRC32: Optional[ChecksumCRC32]
    ChecksumCRC32C: Optional[ChecksumCRC32C]
    ChecksumCRC64NVME: Optional[ChecksumCRC64NVME]
    ChecksumSHA1: Optional[ChecksumSHA1]
    ChecksumSHA256: Optional[ChecksumSHA256]


Parts = List[Part]


class ListPartsOutput(TypedDict, total=False):
    AbortDate: Optional[AbortDate]
    AbortRuleId: Optional[AbortRuleId]
    Bucket: Optional[BucketName]
    Key: Optional[ObjectKey]
    UploadId: Optional[MultipartUploadId]
    PartNumberMarker: Optional[PartNumberMarker]
    NextPartNumberMarker: Optional[NextPartNumberMarker]
    MaxParts: Optional[MaxParts]
    IsTruncated: Optional[IsTruncated]
    Parts: Optional[Parts]
    Initiator: Optional[Initiator]
    Owner: Optional[Owner]
    StorageClass: Optional[StorageClass]
    RequestCharged: Optional[RequestCharged]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    ChecksumType: Optional[ChecksumType]


class ListPartsRequest(ServiceRequest):
    Bucket: BucketName
    Key: ObjectKey
    MaxParts: Optional[MaxParts]
    PartNumberMarker: Optional[PartNumberMarker]
    UploadId: MultipartUploadId
    RequestPayer: Optional[RequestPayer]
    ExpectedBucketOwner: Optional[AccountId]
    SSECustomerAlgorithm: Optional[SSECustomerAlgorithm]
    SSECustomerKey: Optional[SSECustomerKey]
    SSECustomerKeyMD5: Optional[SSECustomerKeyMD5]


class MetadataEntry(TypedDict, total=False):
    Name: Optional[MetadataKey]
    Value: Optional[MetadataValue]


class QueueConfiguration(TypedDict, total=False):
    Id: Optional[NotificationId]
    QueueArn: QueueArn
    Events: EventList
    Filter: Optional[NotificationConfigurationFilter]


QueueConfigurationList = List[QueueConfiguration]


class TopicConfiguration(TypedDict, total=False):
    Id: Optional[NotificationId]
    TopicArn: TopicArn
    Events: EventList
    Filter: Optional[NotificationConfigurationFilter]


TopicConfigurationList = List[TopicConfiguration]


class NotificationConfiguration(TypedDict, total=False):
    TopicConfigurations: Optional[TopicConfigurationList]
    QueueConfigurations: Optional[QueueConfigurationList]
    LambdaFunctionConfigurations: Optional[LambdaFunctionConfigurationList]
    EventBridgeConfiguration: Optional[EventBridgeConfiguration]


class QueueConfigurationDeprecated(TypedDict, total=False):
    Id: Optional[NotificationId]
    Event: Optional[Event]
    Events: Optional[EventList]
    Queue: Optional[QueueArn]


class TopicConfigurationDeprecated(TypedDict, total=False):
    Id: Optional[NotificationId]
    Events: Optional[EventList]
    Event: Optional[Event]
    Topic: Optional[TopicArn]


class NotificationConfigurationDeprecated(TypedDict, total=False):
    TopicConfiguration: Optional[TopicConfigurationDeprecated]
    QueueConfiguration: Optional[QueueConfigurationDeprecated]
    CloudFunctionConfiguration: Optional[CloudFunctionConfiguration]


UserMetadata = List[MetadataEntry]


class Tagging(TypedDict, total=False):
    TagSet: TagSet


class S3Location(TypedDict, total=False):
    BucketName: BucketName
    Prefix: LocationPrefix
    Encryption: Optional[Encryption]
    CannedACL: Optional[ObjectCannedACL]
    AccessControlList: Optional[Grants]
    Tagging: Optional[Tagging]
    UserMetadata: Optional[UserMetadata]
    StorageClass: Optional[StorageClass]


class OutputLocation(TypedDict, total=False):
    S3: Optional[S3Location]


class OutputSerialization(TypedDict, total=False):
    CSV: Optional[CSVOutput]
    JSON: Optional[JSONOutput]


class Progress(TypedDict, total=False):
    BytesScanned: Optional[BytesScanned]
    BytesProcessed: Optional[BytesProcessed]
    BytesReturned: Optional[BytesReturned]


class ProgressEvent(TypedDict, total=False):
    Details: Optional[Progress]


class PutBucketAccelerateConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    AccelerateConfiguration: AccelerateConfiguration
    ExpectedBucketOwner: Optional[AccountId]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]


class PutBucketAclRequest(ServiceRequest):
    ACL: Optional[BucketCannedACL]
    AccessControlPolicy: Optional[AccessControlPolicy]
    Bucket: BucketName
    ContentMD5: Optional[ContentMD5]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    GrantFullControl: Optional[GrantFullControl]
    GrantRead: Optional[GrantRead]
    GrantReadACP: Optional[GrantReadACP]
    GrantWrite: Optional[GrantWrite]
    GrantWriteACP: Optional[GrantWriteACP]
    ExpectedBucketOwner: Optional[AccountId]


class PutBucketAnalyticsConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    Id: AnalyticsId
    AnalyticsConfiguration: AnalyticsConfiguration
    ExpectedBucketOwner: Optional[AccountId]


class PutBucketCorsRequest(ServiceRequest):
    Bucket: BucketName
    CORSConfiguration: CORSConfiguration
    ContentMD5: Optional[ContentMD5]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    ExpectedBucketOwner: Optional[AccountId]


class PutBucketEncryptionRequest(ServiceRequest):
    Bucket: BucketName
    ContentMD5: Optional[ContentMD5]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    ServerSideEncryptionConfiguration: ServerSideEncryptionConfiguration
    ExpectedBucketOwner: Optional[AccountId]


class PutBucketIntelligentTieringConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    Id: IntelligentTieringId
    ExpectedBucketOwner: Optional[AccountId]
    IntelligentTieringConfiguration: IntelligentTieringConfiguration


class PutBucketInventoryConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    Id: InventoryId
    InventoryConfiguration: InventoryConfiguration
    ExpectedBucketOwner: Optional[AccountId]


class PutBucketLifecycleConfigurationOutput(TypedDict, total=False):
    TransitionDefaultMinimumObjectSize: Optional[TransitionDefaultMinimumObjectSize]


class PutBucketLifecycleConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    LifecycleConfiguration: Optional[BucketLifecycleConfiguration]
    ExpectedBucketOwner: Optional[AccountId]
    TransitionDefaultMinimumObjectSize: Optional[TransitionDefaultMinimumObjectSize]


class PutBucketLifecycleRequest(ServiceRequest):
    Bucket: BucketName
    ContentMD5: Optional[ContentMD5]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    LifecycleConfiguration: Optional[LifecycleConfiguration]
    ExpectedBucketOwner: Optional[AccountId]


class PutBucketLoggingRequest(ServiceRequest):
    Bucket: BucketName
    BucketLoggingStatus: BucketLoggingStatus
    ContentMD5: Optional[ContentMD5]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    ExpectedBucketOwner: Optional[AccountId]


class PutBucketMetricsConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    Id: MetricsId
    MetricsConfiguration: MetricsConfiguration
    ExpectedBucketOwner: Optional[AccountId]


class PutBucketNotificationConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    NotificationConfiguration: NotificationConfiguration
    ExpectedBucketOwner: Optional[AccountId]
    SkipDestinationValidation: Optional[SkipValidation]


class PutBucketNotificationRequest(ServiceRequest):
    Bucket: BucketName
    ContentMD5: Optional[ContentMD5]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    NotificationConfiguration: NotificationConfigurationDeprecated
    ExpectedBucketOwner: Optional[AccountId]


class PutBucketOwnershipControlsRequest(ServiceRequest):
    Bucket: BucketName
    ContentMD5: Optional[ContentMD5]
    ExpectedBucketOwner: Optional[AccountId]
    OwnershipControls: OwnershipControls
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]


class PutBucketPolicyRequest(ServiceRequest):
    Bucket: BucketName
    ContentMD5: Optional[ContentMD5]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    ConfirmRemoveSelfBucketAccess: Optional[ConfirmRemoveSelfBucketAccess]
    Policy: Policy
    ExpectedBucketOwner: Optional[AccountId]


class PutBucketReplicationRequest(ServiceRequest):
    Bucket: BucketName
    ContentMD5: Optional[ContentMD5]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    ReplicationConfiguration: ReplicationConfiguration
    Token: Optional[ObjectLockToken]
    ExpectedBucketOwner: Optional[AccountId]


class RequestPaymentConfiguration(TypedDict, total=False):
    Payer: Payer


class PutBucketRequestPaymentRequest(ServiceRequest):
    Bucket: BucketName
    ContentMD5: Optional[ContentMD5]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    RequestPaymentConfiguration: RequestPaymentConfiguration
    ExpectedBucketOwner: Optional[AccountId]


class PutBucketTaggingRequest(ServiceRequest):
    Bucket: BucketName
    ContentMD5: Optional[ContentMD5]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    Tagging: Tagging
    ExpectedBucketOwner: Optional[AccountId]


class VersioningConfiguration(TypedDict, total=False):
    MFADelete: Optional[MFADelete]
    Status: Optional[BucketVersioningStatus]


class PutBucketVersioningRequest(ServiceRequest):
    Bucket: BucketName
    ContentMD5: Optional[ContentMD5]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    MFA: Optional[MFA]
    VersioningConfiguration: VersioningConfiguration
    ExpectedBucketOwner: Optional[AccountId]


class WebsiteConfiguration(TypedDict, total=False):
    ErrorDocument: Optional[ErrorDocument]
    IndexDocument: Optional[IndexDocument]
    RedirectAllRequestsTo: Optional[RedirectAllRequestsTo]
    RoutingRules: Optional[RoutingRules]


class PutBucketWebsiteRequest(ServiceRequest):
    Bucket: BucketName
    ContentMD5: Optional[ContentMD5]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    WebsiteConfiguration: WebsiteConfiguration
    ExpectedBucketOwner: Optional[AccountId]


class PutObjectAclOutput(TypedDict, total=False):
    RequestCharged: Optional[RequestCharged]


class PutObjectAclRequest(ServiceRequest):
    ACL: Optional[ObjectCannedACL]
    AccessControlPolicy: Optional[AccessControlPolicy]
    Bucket: BucketName
    ContentMD5: Optional[ContentMD5]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    GrantFullControl: Optional[GrantFullControl]
    GrantRead: Optional[GrantRead]
    GrantReadACP: Optional[GrantReadACP]
    GrantWrite: Optional[GrantWrite]
    GrantWriteACP: Optional[GrantWriteACP]
    Key: ObjectKey
    RequestPayer: Optional[RequestPayer]
    VersionId: Optional[ObjectVersionId]
    ExpectedBucketOwner: Optional[AccountId]


class PutObjectLegalHoldOutput(TypedDict, total=False):
    RequestCharged: Optional[RequestCharged]


class PutObjectLegalHoldRequest(ServiceRequest):
    Bucket: BucketName
    Key: ObjectKey
    LegalHold: Optional[ObjectLockLegalHold]
    RequestPayer: Optional[RequestPayer]
    VersionId: Optional[ObjectVersionId]
    ContentMD5: Optional[ContentMD5]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    ExpectedBucketOwner: Optional[AccountId]


class PutObjectLockConfigurationOutput(TypedDict, total=False):
    RequestCharged: Optional[RequestCharged]


class PutObjectLockConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    ObjectLockConfiguration: Optional[ObjectLockConfiguration]
    RequestPayer: Optional[RequestPayer]
    Token: Optional[ObjectLockToken]
    ContentMD5: Optional[ContentMD5]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    ExpectedBucketOwner: Optional[AccountId]


class PutObjectOutput(TypedDict, total=False):
    Expiration: Optional[Expiration]
    ETag: Optional[ETag]
    ChecksumCRC32: Optional[ChecksumCRC32]
    ChecksumCRC32C: Optional[ChecksumCRC32C]
    ChecksumCRC64NVME: Optional[ChecksumCRC64NVME]
    ChecksumSHA1: Optional[ChecksumSHA1]
    ChecksumSHA256: Optional[ChecksumSHA256]
    ChecksumType: Optional[ChecksumType]
    ServerSideEncryption: Optional[ServerSideEncryption]
    VersionId: Optional[ObjectVersionId]
    SSECustomerAlgorithm: Optional[SSECustomerAlgorithm]
    SSECustomerKeyMD5: Optional[SSECustomerKeyMD5]
    SSEKMSKeyId: Optional[SSEKMSKeyId]
    SSEKMSEncryptionContext: Optional[SSEKMSEncryptionContext]
    BucketKeyEnabled: Optional[BucketKeyEnabled]
    Size: Optional[Size]
    RequestCharged: Optional[RequestCharged]


WriteOffsetBytes = int


class PutObjectRequest(ServiceRequest):
    Body: Optional[IO[Body]]
    ACL: Optional[ObjectCannedACL]
    Bucket: BucketName
    CacheControl: Optional[CacheControl]
    ContentDisposition: Optional[ContentDisposition]
    ContentEncoding: Optional[ContentEncoding]
    ContentLanguage: Optional[ContentLanguage]
    ContentLength: Optional[ContentLength]
    ContentMD5: Optional[ContentMD5]
    ContentType: Optional[ContentType]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    ChecksumCRC32: Optional[ChecksumCRC32]
    ChecksumCRC32C: Optional[ChecksumCRC32C]
    ChecksumCRC64NVME: Optional[ChecksumCRC64NVME]
    ChecksumSHA1: Optional[ChecksumSHA1]
    ChecksumSHA256: Optional[ChecksumSHA256]
    Expires: Optional[Expires]
    IfMatch: Optional[IfMatch]
    IfNoneMatch: Optional[IfNoneMatch]
    GrantFullControl: Optional[GrantFullControl]
    GrantRead: Optional[GrantRead]
    GrantReadACP: Optional[GrantReadACP]
    GrantWriteACP: Optional[GrantWriteACP]
    Key: ObjectKey
    WriteOffsetBytes: Optional[WriteOffsetBytes]
    Metadata: Optional[Metadata]
    ServerSideEncryption: Optional[ServerSideEncryption]
    StorageClass: Optional[StorageClass]
    WebsiteRedirectLocation: Optional[WebsiteRedirectLocation]
    SSECustomerAlgorithm: Optional[SSECustomerAlgorithm]
    SSECustomerKey: Optional[SSECustomerKey]
    SSECustomerKeyMD5: Optional[SSECustomerKeyMD5]
    SSEKMSKeyId: Optional[SSEKMSKeyId]
    SSEKMSEncryptionContext: Optional[SSEKMSEncryptionContext]
    BucketKeyEnabled: Optional[BucketKeyEnabled]
    RequestPayer: Optional[RequestPayer]
    Tagging: Optional[TaggingHeader]
    ObjectLockMode: Optional[ObjectLockMode]
    ObjectLockRetainUntilDate: Optional[ObjectLockRetainUntilDate]
    ObjectLockLegalHoldStatus: Optional[ObjectLockLegalHoldStatus]
    ExpectedBucketOwner: Optional[AccountId]


class PutObjectRetentionOutput(TypedDict, total=False):
    RequestCharged: Optional[RequestCharged]


class PutObjectRetentionRequest(ServiceRequest):
    Bucket: BucketName
    Key: ObjectKey
    Retention: Optional[ObjectLockRetention]
    RequestPayer: Optional[RequestPayer]
    VersionId: Optional[ObjectVersionId]
    BypassGovernanceRetention: Optional[BypassGovernanceRetention]
    ContentMD5: Optional[ContentMD5]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    ExpectedBucketOwner: Optional[AccountId]


class PutObjectTaggingOutput(TypedDict, total=False):
    VersionId: Optional[ObjectVersionId]


class PutObjectTaggingRequest(ServiceRequest):
    Bucket: BucketName
    Key: ObjectKey
    VersionId: Optional[ObjectVersionId]
    ContentMD5: Optional[ContentMD5]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    Tagging: Tagging
    ExpectedBucketOwner: Optional[AccountId]
    RequestPayer: Optional[RequestPayer]


class PutPublicAccessBlockRequest(ServiceRequest):
    Bucket: BucketName
    ContentMD5: Optional[ContentMD5]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    PublicAccessBlockConfiguration: PublicAccessBlockConfiguration
    ExpectedBucketOwner: Optional[AccountId]


class RecordsEvent(TypedDict, total=False):
    Payload: Optional[Body]


class RenameObjectOutput(TypedDict, total=False):
    pass


RenameSourceIfUnmodifiedSince = datetime
RenameSourceIfModifiedSince = datetime


class RenameObjectRequest(ServiceRequest):
    Bucket: BucketName
    Key: ObjectKey
    RenameSource: RenameSource
    DestinationIfMatch: Optional[IfMatch]
    DestinationIfNoneMatch: Optional[IfNoneMatch]
    DestinationIfModifiedSince: Optional[IfModifiedSince]
    DestinationIfUnmodifiedSince: Optional[IfUnmodifiedSince]
    SourceIfMatch: Optional[RenameSourceIfMatch]
    SourceIfNoneMatch: Optional[RenameSourceIfNoneMatch]
    SourceIfModifiedSince: Optional[RenameSourceIfModifiedSince]
    SourceIfUnmodifiedSince: Optional[RenameSourceIfUnmodifiedSince]
    ClientToken: Optional[ClientToken]


class RequestProgress(TypedDict, total=False):
    Enabled: Optional[EnableRequestProgress]


class RestoreObjectOutput(TypedDict, total=False):
    RequestCharged: Optional[RequestCharged]
    RestoreOutputPath: Optional[RestoreOutputPath]
    StatusCode: Optional[RestoreObjectOutputStatusCode]


class SelectParameters(TypedDict, total=False):
    InputSerialization: InputSerialization
    ExpressionType: ExpressionType
    Expression: Expression
    OutputSerialization: OutputSerialization


class RestoreRequest(TypedDict, total=False):
    Days: Optional[Days]
    GlacierJobParameters: Optional[GlacierJobParameters]
    Type: Optional[RestoreRequestType]
    Tier: Optional[Tier]
    Description: Optional[Description]
    SelectParameters: Optional[SelectParameters]
    OutputLocation: Optional[OutputLocation]


class RestoreObjectRequest(ServiceRequest):
    Bucket: BucketName
    Key: ObjectKey
    VersionId: Optional[ObjectVersionId]
    RestoreRequest: Optional[RestoreRequest]
    RequestPayer: Optional[RequestPayer]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    ExpectedBucketOwner: Optional[AccountId]


Start = int


class ScanRange(TypedDict, total=False):
    Start: Optional[Start]
    End: Optional[End]


class Stats(TypedDict, total=False):
    BytesScanned: Optional[BytesScanned]
    BytesProcessed: Optional[BytesProcessed]
    BytesReturned: Optional[BytesReturned]


class StatsEvent(TypedDict, total=False):
    Details: Optional[Stats]


class SelectObjectContentEventStream(TypedDict, total=False):
    Records: Optional[RecordsEvent]
    Stats: Optional[StatsEvent]
    Progress: Optional[ProgressEvent]
    Cont: Optional[ContinuationEvent]
    End: Optional[EndEvent]


class SelectObjectContentOutput(TypedDict, total=False):
    Payload: Iterator[SelectObjectContentEventStream]


class SelectObjectContentRequest(ServiceRequest):
    Bucket: BucketName
    Key: ObjectKey
    SSECustomerAlgorithm: Optional[SSECustomerAlgorithm]
    SSECustomerKey: Optional[SSECustomerKey]
    SSECustomerKeyMD5: Optional[SSECustomerKeyMD5]
    Expression: Expression
    ExpressionType: ExpressionType
    RequestProgress: Optional[RequestProgress]
    InputSerialization: InputSerialization
    OutputSerialization: OutputSerialization
    ScanRange: Optional[ScanRange]
    ExpectedBucketOwner: Optional[AccountId]


class UpdateBucketMetadataInventoryTableConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    ContentMD5: Optional[ContentMD5]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    InventoryTableConfiguration: InventoryTableConfigurationUpdates
    ExpectedBucketOwner: Optional[AccountId]


class UpdateBucketMetadataJournalTableConfigurationRequest(ServiceRequest):
    Bucket: BucketName
    ContentMD5: Optional[ContentMD5]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    JournalTableConfiguration: JournalTableConfigurationUpdates
    ExpectedBucketOwner: Optional[AccountId]


class UploadPartCopyOutput(TypedDict, total=False):
    CopySourceVersionId: Optional[CopySourceVersionId]
    CopyPartResult: Optional[CopyPartResult]
    ServerSideEncryption: Optional[ServerSideEncryption]
    SSECustomerAlgorithm: Optional[SSECustomerAlgorithm]
    SSECustomerKeyMD5: Optional[SSECustomerKeyMD5]
    SSEKMSKeyId: Optional[SSEKMSKeyId]
    BucketKeyEnabled: Optional[BucketKeyEnabled]
    RequestCharged: Optional[RequestCharged]


class UploadPartCopyRequest(ServiceRequest):
    Bucket: BucketName
    CopySource: CopySource
    CopySourceIfMatch: Optional[CopySourceIfMatch]
    CopySourceIfModifiedSince: Optional[CopySourceIfModifiedSince]
    CopySourceIfNoneMatch: Optional[CopySourceIfNoneMatch]
    CopySourceIfUnmodifiedSince: Optional[CopySourceIfUnmodifiedSince]
    CopySourceRange: Optional[CopySourceRange]
    Key: ObjectKey
    PartNumber: PartNumber
    UploadId: MultipartUploadId
    SSECustomerAlgorithm: Optional[SSECustomerAlgorithm]
    SSECustomerKey: Optional[SSECustomerKey]
    SSECustomerKeyMD5: Optional[SSECustomerKeyMD5]
    CopySourceSSECustomerAlgorithm: Optional[CopySourceSSECustomerAlgorithm]
    CopySourceSSECustomerKey: Optional[CopySourceSSECustomerKey]
    CopySourceSSECustomerKeyMD5: Optional[CopySourceSSECustomerKeyMD5]
    RequestPayer: Optional[RequestPayer]
    ExpectedBucketOwner: Optional[AccountId]
    ExpectedSourceBucketOwner: Optional[AccountId]


class UploadPartOutput(TypedDict, total=False):
    ServerSideEncryption: Optional[ServerSideEncryption]
    ETag: Optional[ETag]
    ChecksumCRC32: Optional[ChecksumCRC32]
    ChecksumCRC32C: Optional[ChecksumCRC32C]
    ChecksumCRC64NVME: Optional[ChecksumCRC64NVME]
    ChecksumSHA1: Optional[ChecksumSHA1]
    ChecksumSHA256: Optional[ChecksumSHA256]
    SSECustomerAlgorithm: Optional[SSECustomerAlgorithm]
    SSECustomerKeyMD5: Optional[SSECustomerKeyMD5]
    SSEKMSKeyId: Optional[SSEKMSKeyId]
    BucketKeyEnabled: Optional[BucketKeyEnabled]
    RequestCharged: Optional[RequestCharged]


class UploadPartRequest(ServiceRequest):
    Body: Optional[IO[Body]]
    Bucket: BucketName
    ContentLength: Optional[ContentLength]
    ContentMD5: Optional[ContentMD5]
    ChecksumAlgorithm: Optional[ChecksumAlgorithm]
    ChecksumCRC32: Optional[ChecksumCRC32]
    ChecksumCRC32C: Optional[ChecksumCRC32C]
    ChecksumCRC64NVME: Optional[ChecksumCRC64NVME]
    ChecksumSHA1: Optional[ChecksumSHA1]
    ChecksumSHA256: Optional[ChecksumSHA256]
    Key: ObjectKey
    PartNumber: PartNumber
    UploadId: MultipartUploadId
    SSECustomerAlgorithm: Optional[SSECustomerAlgorithm]
    SSECustomerKey: Optional[SSECustomerKey]
    SSECustomerKeyMD5: Optional[SSECustomerKeyMD5]
    RequestPayer: Optional[RequestPayer]
    ExpectedBucketOwner: Optional[AccountId]


class WriteGetObjectResponseRequest(ServiceRequest):
    Body: Optional[IO[Body]]
    RequestRoute: RequestRoute
    RequestToken: RequestToken
    StatusCode: Optional[GetObjectResponseStatusCode]
    ErrorCode: Optional[ErrorCode]
    ErrorMessage: Optional[ErrorMessage]
    AcceptRanges: Optional[AcceptRanges]
    CacheControl: Optional[CacheControl]
    ContentDisposition: Optional[ContentDisposition]
    ContentEncoding: Optional[ContentEncoding]
    ContentLanguage: Optional[ContentLanguage]
    ContentLength: Optional[ContentLength]
    ContentRange: Optional[ContentRange]
    ContentType: Optional[ContentType]
    ChecksumCRC32: Optional[ChecksumCRC32]
    ChecksumCRC32C: Optional[ChecksumCRC32C]
    ChecksumCRC64NVME: Optional[ChecksumCRC64NVME]
    ChecksumSHA1: Optional[ChecksumSHA1]
    ChecksumSHA256: Optional[ChecksumSHA256]
    DeleteMarker: Optional[DeleteMarker]
    ETag: Optional[ETag]
    Expires: Optional[Expires]
    Expiration: Optional[Expiration]
    LastModified: Optional[LastModified]
    MissingMeta: Optional[MissingMeta]
    Metadata: Optional[Metadata]
    ObjectLockMode: Optional[ObjectLockMode]
    ObjectLockLegalHoldStatus: Optional[ObjectLockLegalHoldStatus]
    ObjectLockRetainUntilDate: Optional[ObjectLockRetainUntilDate]
    PartsCount: Optional[PartsCount]
    ReplicationStatus: Optional[ReplicationStatus]
    RequestCharged: Optional[RequestCharged]
    Restore: Optional[Restore]
    ServerSideEncryption: Optional[ServerSideEncryption]
    SSECustomerAlgorithm: Optional[SSECustomerAlgorithm]
    SSEKMSKeyId: Optional[SSEKMSKeyId]
    SSECustomerKeyMD5: Optional[SSECustomerKeyMD5]
    StorageClass: Optional[StorageClass]
    TagCount: Optional[TagCount]
    VersionId: Optional[ObjectVersionId]
    BucketKeyEnabled: Optional[BucketKeyEnabled]


class PostObjectRequest(ServiceRequest):
    Body: Optional[IO[Body]]
    Bucket: BucketName


class PostResponse(TypedDict, total=False):
    StatusCode: Optional[GetObjectResponseStatusCode]
    Location: Optional[Location]
    LocationHeader: Optional[Location]
    Bucket: Optional[BucketName]
    Key: Optional[ObjectKey]
    Expiration: Optional[Expiration]
    ETag: Optional[ETag]
    ETagHeader: Optional[ETag]
    ChecksumCRC32: Optional[ChecksumCRC32]
    ChecksumCRC32C: Optional[ChecksumCRC32C]
    ChecksumCRC64NVME: Optional[ChecksumCRC64NVME]
    ChecksumSHA1: Optional[ChecksumSHA1]
    ChecksumSHA256: Optional[ChecksumSHA256]
    ChecksumType: Optional[ChecksumType]
    ServerSideEncryption: Optional[ServerSideEncryption]
    VersionId: Optional[ObjectVersionId]
    SSECustomerAlgorithm: Optional[SSECustomerAlgorithm]
    SSECustomerKeyMD5: Optional[SSECustomerKeyMD5]
    SSEKMSKeyId: Optional[SSEKMSKeyId]
    SSEKMSEncryptionContext: Optional[SSEKMSEncryptionContext]
    BucketKeyEnabled: Optional[BucketKeyEnabled]
    RequestCharged: Optional[RequestCharged]


class S3Api:
    service = "s3"
    version = "2006-03-01"

    @handler("AbortMultipartUpload")
    def abort_multipart_upload(
        self,
        context: RequestContext,
        bucket: BucketName,
        key: ObjectKey,
        upload_id: MultipartUploadId,
        request_payer: RequestPayer | None = None,
        expected_bucket_owner: AccountId | None = None,
        if_match_initiated_time: IfMatchInitiatedTime | None = None,
        **kwargs,
    ) -> AbortMultipartUploadOutput:
        raise NotImplementedError

    @handler("CompleteMultipartUpload")
    def complete_multipart_upload(
        self,
        context: RequestContext,
        bucket: BucketName,
        key: ObjectKey,
        upload_id: MultipartUploadId,
        multipart_upload: CompletedMultipartUpload | None = None,
        checksum_crc32: ChecksumCRC32 | None = None,
        checksum_crc32_c: ChecksumCRC32C | None = None,
        checksum_crc64_nvme: ChecksumCRC64NVME | None = None,
        checksum_sha1: ChecksumSHA1 | None = None,
        checksum_sha256: ChecksumSHA256 | None = None,
        checksum_type: ChecksumType | None = None,
        mpu_object_size: MpuObjectSize | None = None,
        request_payer: RequestPayer | None = None,
        expected_bucket_owner: AccountId | None = None,
        if_match: IfMatch | None = None,
        if_none_match: IfNoneMatch | None = None,
        sse_customer_algorithm: SSECustomerAlgorithm | None = None,
        sse_customer_key: SSECustomerKey | None = None,
        sse_customer_key_md5: SSECustomerKeyMD5 | None = None,
        **kwargs,
    ) -> CompleteMultipartUploadOutput:
        raise NotImplementedError

    @handler("CopyObject")
    def copy_object(
        self,
        context: RequestContext,
        bucket: BucketName,
        copy_source: CopySource,
        key: ObjectKey,
        acl: ObjectCannedACL | None = None,
        cache_control: CacheControl | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        content_disposition: ContentDisposition | None = None,
        content_encoding: ContentEncoding | None = None,
        content_language: ContentLanguage | None = None,
        content_type: ContentType | None = None,
        copy_source_if_match: CopySourceIfMatch | None = None,
        copy_source_if_modified_since: CopySourceIfModifiedSince | None = None,
        copy_source_if_none_match: CopySourceIfNoneMatch | None = None,
        copy_source_if_unmodified_since: CopySourceIfUnmodifiedSince | None = None,
        expires: Expires | None = None,
        grant_full_control: GrantFullControl | None = None,
        grant_read: GrantRead | None = None,
        grant_read_acp: GrantReadACP | None = None,
        grant_write_acp: GrantWriteACP | None = None,
        metadata: Metadata | None = None,
        metadata_directive: MetadataDirective | None = None,
        tagging_directive: TaggingDirective | None = None,
        server_side_encryption: ServerSideEncryption | None = None,
        storage_class: StorageClass | None = None,
        website_redirect_location: WebsiteRedirectLocation | None = None,
        sse_customer_algorithm: SSECustomerAlgorithm | None = None,
        sse_customer_key: SSECustomerKey | None = None,
        sse_customer_key_md5: SSECustomerKeyMD5 | None = None,
        ssekms_key_id: SSEKMSKeyId | None = None,
        ssekms_encryption_context: SSEKMSEncryptionContext | None = None,
        bucket_key_enabled: BucketKeyEnabled | None = None,
        copy_source_sse_customer_algorithm: CopySourceSSECustomerAlgorithm | None = None,
        copy_source_sse_customer_key: CopySourceSSECustomerKey | None = None,
        copy_source_sse_customer_key_md5: CopySourceSSECustomerKeyMD5 | None = None,
        request_payer: RequestPayer | None = None,
        tagging: TaggingHeader | None = None,
        object_lock_mode: ObjectLockMode | None = None,
        object_lock_retain_until_date: ObjectLockRetainUntilDate | None = None,
        object_lock_legal_hold_status: ObjectLockLegalHoldStatus | None = None,
        expected_bucket_owner: AccountId | None = None,
        expected_source_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> CopyObjectOutput:
        raise NotImplementedError

    @handler("CreateBucket")
    def create_bucket(
        self,
        context: RequestContext,
        bucket: BucketName,
        acl: BucketCannedACL | None = None,
        create_bucket_configuration: CreateBucketConfiguration | None = None,
        grant_full_control: GrantFullControl | None = None,
        grant_read: GrantRead | None = None,
        grant_read_acp: GrantReadACP | None = None,
        grant_write: GrantWrite | None = None,
        grant_write_acp: GrantWriteACP | None = None,
        object_lock_enabled_for_bucket: ObjectLockEnabledForBucket | None = None,
        object_ownership: ObjectOwnership | None = None,
        **kwargs,
    ) -> CreateBucketOutput:
        raise NotImplementedError

    @handler("CreateBucketMetadataConfiguration")
    def create_bucket_metadata_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        metadata_configuration: MetadataConfiguration,
        content_md5: ContentMD5 | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("CreateBucketMetadataTableConfiguration")
    def create_bucket_metadata_table_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        metadata_table_configuration: MetadataTableConfiguration,
        content_md5: ContentMD5 | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("CreateMultipartUpload")
    def create_multipart_upload(
        self,
        context: RequestContext,
        bucket: BucketName,
        key: ObjectKey,
        acl: ObjectCannedACL | None = None,
        cache_control: CacheControl | None = None,
        content_disposition: ContentDisposition | None = None,
        content_encoding: ContentEncoding | None = None,
        content_language: ContentLanguage | None = None,
        content_type: ContentType | None = None,
        expires: Expires | None = None,
        grant_full_control: GrantFullControl | None = None,
        grant_read: GrantRead | None = None,
        grant_read_acp: GrantReadACP | None = None,
        grant_write_acp: GrantWriteACP | None = None,
        metadata: Metadata | None = None,
        server_side_encryption: ServerSideEncryption | None = None,
        storage_class: StorageClass | None = None,
        website_redirect_location: WebsiteRedirectLocation | None = None,
        sse_customer_algorithm: SSECustomerAlgorithm | None = None,
        sse_customer_key: SSECustomerKey | None = None,
        sse_customer_key_md5: SSECustomerKeyMD5 | None = None,
        ssekms_key_id: SSEKMSKeyId | None = None,
        ssekms_encryption_context: SSEKMSEncryptionContext | None = None,
        bucket_key_enabled: BucketKeyEnabled | None = None,
        request_payer: RequestPayer | None = None,
        tagging: TaggingHeader | None = None,
        object_lock_mode: ObjectLockMode | None = None,
        object_lock_retain_until_date: ObjectLockRetainUntilDate | None = None,
        object_lock_legal_hold_status: ObjectLockLegalHoldStatus | None = None,
        expected_bucket_owner: AccountId | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        checksum_type: ChecksumType | None = None,
        **kwargs,
    ) -> CreateMultipartUploadOutput:
        raise NotImplementedError

    @handler("CreateSession")
    def create_session(
        self,
        context: RequestContext,
        bucket: BucketName,
        session_mode: SessionMode | None = None,
        server_side_encryption: ServerSideEncryption | None = None,
        ssekms_key_id: SSEKMSKeyId | None = None,
        ssekms_encryption_context: SSEKMSEncryptionContext | None = None,
        bucket_key_enabled: BucketKeyEnabled | None = None,
        **kwargs,
    ) -> CreateSessionOutput:
        raise NotImplementedError

    @handler("DeleteBucket")
    def delete_bucket(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("DeleteBucketAnalyticsConfiguration")
    def delete_bucket_analytics_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        id: AnalyticsId,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("DeleteBucketCors")
    def delete_bucket_cors(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("DeleteBucketEncryption")
    def delete_bucket_encryption(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("DeleteBucketIntelligentTieringConfiguration")
    def delete_bucket_intelligent_tiering_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        id: IntelligentTieringId,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("DeleteBucketInventoryConfiguration")
    def delete_bucket_inventory_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        id: InventoryId,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("DeleteBucketLifecycle")
    def delete_bucket_lifecycle(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("DeleteBucketMetadataConfiguration")
    def delete_bucket_metadata_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("DeleteBucketMetadataTableConfiguration")
    def delete_bucket_metadata_table_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("DeleteBucketMetricsConfiguration")
    def delete_bucket_metrics_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        id: MetricsId,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("DeleteBucketOwnershipControls")
    def delete_bucket_ownership_controls(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("DeleteBucketPolicy")
    def delete_bucket_policy(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("DeleteBucketReplication")
    def delete_bucket_replication(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("DeleteBucketTagging")
    def delete_bucket_tagging(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("DeleteBucketWebsite")
    def delete_bucket_website(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("DeleteObject")
    def delete_object(
        self,
        context: RequestContext,
        bucket: BucketName,
        key: ObjectKey,
        mfa: MFA | None = None,
        version_id: ObjectVersionId | None = None,
        request_payer: RequestPayer | None = None,
        bypass_governance_retention: BypassGovernanceRetention | None = None,
        expected_bucket_owner: AccountId | None = None,
        if_match: IfMatch | None = None,
        if_match_last_modified_time: IfMatchLastModifiedTime | None = None,
        if_match_size: IfMatchSize | None = None,
        **kwargs,
    ) -> DeleteObjectOutput:
        raise NotImplementedError

    @handler("DeleteObjectTagging")
    def delete_object_tagging(
        self,
        context: RequestContext,
        bucket: BucketName,
        key: ObjectKey,
        version_id: ObjectVersionId | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> DeleteObjectTaggingOutput:
        raise NotImplementedError

    @handler("DeleteObjects")
    def delete_objects(
        self,
        context: RequestContext,
        bucket: BucketName,
        delete: Delete,
        mfa: MFA | None = None,
        request_payer: RequestPayer | None = None,
        bypass_governance_retention: BypassGovernanceRetention | None = None,
        expected_bucket_owner: AccountId | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        **kwargs,
    ) -> DeleteObjectsOutput:
        raise NotImplementedError

    @handler("DeletePublicAccessBlock")
    def delete_public_access_block(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("GetBucketAccelerateConfiguration")
    def get_bucket_accelerate_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        request_payer: RequestPayer | None = None,
        **kwargs,
    ) -> GetBucketAccelerateConfigurationOutput:
        raise NotImplementedError

    @handler("GetBucketAcl")
    def get_bucket_acl(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetBucketAclOutput:
        raise NotImplementedError

    @handler("GetBucketAnalyticsConfiguration")
    def get_bucket_analytics_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        id: AnalyticsId,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetBucketAnalyticsConfigurationOutput:
        raise NotImplementedError

    @handler("GetBucketCors")
    def get_bucket_cors(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetBucketCorsOutput:
        raise NotImplementedError

    @handler("GetBucketEncryption")
    def get_bucket_encryption(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetBucketEncryptionOutput:
        raise NotImplementedError

    @handler("GetBucketIntelligentTieringConfiguration")
    def get_bucket_intelligent_tiering_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        id: IntelligentTieringId,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetBucketIntelligentTieringConfigurationOutput:
        raise NotImplementedError

    @handler("GetBucketInventoryConfiguration")
    def get_bucket_inventory_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        id: InventoryId,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetBucketInventoryConfigurationOutput:
        raise NotImplementedError

    @handler("GetBucketLifecycle")
    def get_bucket_lifecycle(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetBucketLifecycleOutput:
        raise NotImplementedError

    @handler("GetBucketLifecycleConfiguration")
    def get_bucket_lifecycle_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetBucketLifecycleConfigurationOutput:
        raise NotImplementedError

    @handler("GetBucketLocation")
    def get_bucket_location(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetBucketLocationOutput:
        raise NotImplementedError

    @handler("GetBucketLogging")
    def get_bucket_logging(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetBucketLoggingOutput:
        raise NotImplementedError

    @handler("GetBucketMetadataConfiguration")
    def get_bucket_metadata_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetBucketMetadataConfigurationOutput:
        raise NotImplementedError

    @handler("GetBucketMetadataTableConfiguration")
    def get_bucket_metadata_table_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetBucketMetadataTableConfigurationOutput:
        raise NotImplementedError

    @handler("GetBucketMetricsConfiguration")
    def get_bucket_metrics_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        id: MetricsId,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetBucketMetricsConfigurationOutput:
        raise NotImplementedError

    @handler("GetBucketNotification")
    def get_bucket_notification(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> NotificationConfigurationDeprecated:
        raise NotImplementedError

    @handler("GetBucketNotificationConfiguration")
    def get_bucket_notification_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> NotificationConfiguration:
        raise NotImplementedError

    @handler("GetBucketOwnershipControls")
    def get_bucket_ownership_controls(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetBucketOwnershipControlsOutput:
        raise NotImplementedError

    @handler("GetBucketPolicy")
    def get_bucket_policy(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetBucketPolicyOutput:
        raise NotImplementedError

    @handler("GetBucketPolicyStatus")
    def get_bucket_policy_status(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetBucketPolicyStatusOutput:
        raise NotImplementedError

    @handler("GetBucketReplication")
    def get_bucket_replication(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetBucketReplicationOutput:
        raise NotImplementedError

    @handler("GetBucketRequestPayment")
    def get_bucket_request_payment(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetBucketRequestPaymentOutput:
        raise NotImplementedError

    @handler("GetBucketTagging")
    def get_bucket_tagging(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetBucketTaggingOutput:
        raise NotImplementedError

    @handler("GetBucketVersioning")
    def get_bucket_versioning(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetBucketVersioningOutput:
        raise NotImplementedError

    @handler("GetBucketWebsite")
    def get_bucket_website(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetBucketWebsiteOutput:
        raise NotImplementedError

    @handler("GetObject")
    def get_object(
        self,
        context: RequestContext,
        bucket: BucketName,
        key: ObjectKey,
        if_match: IfMatch | None = None,
        if_modified_since: IfModifiedSince | None = None,
        if_none_match: IfNoneMatch | None = None,
        if_unmodified_since: IfUnmodifiedSince | None = None,
        range: Range | None = None,
        response_cache_control: ResponseCacheControl | None = None,
        response_content_disposition: ResponseContentDisposition | None = None,
        response_content_encoding: ResponseContentEncoding | None = None,
        response_content_language: ResponseContentLanguage | None = None,
        response_content_type: ResponseContentType | None = None,
        response_expires: ResponseExpires | None = None,
        version_id: ObjectVersionId | None = None,
        sse_customer_algorithm: SSECustomerAlgorithm | None = None,
        sse_customer_key: SSECustomerKey | None = None,
        sse_customer_key_md5: SSECustomerKeyMD5 | None = None,
        request_payer: RequestPayer | None = None,
        part_number: PartNumber | None = None,
        expected_bucket_owner: AccountId | None = None,
        checksum_mode: ChecksumMode | None = None,
        **kwargs,
    ) -> GetObjectOutput:
        raise NotImplementedError

    @handler("GetObjectAcl")
    def get_object_acl(
        self,
        context: RequestContext,
        bucket: BucketName,
        key: ObjectKey,
        version_id: ObjectVersionId | None = None,
        request_payer: RequestPayer | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetObjectAclOutput:
        raise NotImplementedError

    @handler("GetObjectAttributes")
    def get_object_attributes(
        self,
        context: RequestContext,
        bucket: BucketName,
        key: ObjectKey,
        object_attributes: ObjectAttributesList,
        version_id: ObjectVersionId | None = None,
        max_parts: MaxParts | None = None,
        part_number_marker: PartNumberMarker | None = None,
        sse_customer_algorithm: SSECustomerAlgorithm | None = None,
        sse_customer_key: SSECustomerKey | None = None,
        sse_customer_key_md5: SSECustomerKeyMD5 | None = None,
        request_payer: RequestPayer | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetObjectAttributesOutput:
        raise NotImplementedError

    @handler("GetObjectLegalHold")
    def get_object_legal_hold(
        self,
        context: RequestContext,
        bucket: BucketName,
        key: ObjectKey,
        version_id: ObjectVersionId | None = None,
        request_payer: RequestPayer | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetObjectLegalHoldOutput:
        raise NotImplementedError

    @handler("GetObjectLockConfiguration")
    def get_object_lock_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetObjectLockConfigurationOutput:
        raise NotImplementedError

    @handler("GetObjectRetention")
    def get_object_retention(
        self,
        context: RequestContext,
        bucket: BucketName,
        key: ObjectKey,
        version_id: ObjectVersionId | None = None,
        request_payer: RequestPayer | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetObjectRetentionOutput:
        raise NotImplementedError

    @handler("GetObjectTagging")
    def get_object_tagging(
        self,
        context: RequestContext,
        bucket: BucketName,
        key: ObjectKey,
        version_id: ObjectVersionId | None = None,
        expected_bucket_owner: AccountId | None = None,
        request_payer: RequestPayer | None = None,
        **kwargs,
    ) -> GetObjectTaggingOutput:
        raise NotImplementedError

    @handler("GetObjectTorrent")
    def get_object_torrent(
        self,
        context: RequestContext,
        bucket: BucketName,
        key: ObjectKey,
        request_payer: RequestPayer | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetObjectTorrentOutput:
        raise NotImplementedError

    @handler("GetPublicAccessBlock")
    def get_public_access_block(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> GetPublicAccessBlockOutput:
        raise NotImplementedError

    @handler("HeadBucket")
    def head_bucket(
        self,
        context: RequestContext,
        bucket: BucketName,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> HeadBucketOutput:
        raise NotImplementedError

    @handler("HeadObject")
    def head_object(
        self,
        context: RequestContext,
        bucket: BucketName,
        key: ObjectKey,
        if_match: IfMatch | None = None,
        if_modified_since: IfModifiedSince | None = None,
        if_none_match: IfNoneMatch | None = None,
        if_unmodified_since: IfUnmodifiedSince | None = None,
        range: Range | None = None,
        response_cache_control: ResponseCacheControl | None = None,
        response_content_disposition: ResponseContentDisposition | None = None,
        response_content_encoding: ResponseContentEncoding | None = None,
        response_content_language: ResponseContentLanguage | None = None,
        response_content_type: ResponseContentType | None = None,
        response_expires: ResponseExpires | None = None,
        version_id: ObjectVersionId | None = None,
        sse_customer_algorithm: SSECustomerAlgorithm | None = None,
        sse_customer_key: SSECustomerKey | None = None,
        sse_customer_key_md5: SSECustomerKeyMD5 | None = None,
        request_payer: RequestPayer | None = None,
        part_number: PartNumber | None = None,
        expected_bucket_owner: AccountId | None = None,
        checksum_mode: ChecksumMode | None = None,
        **kwargs,
    ) -> HeadObjectOutput:
        raise NotImplementedError

    @handler("ListBucketAnalyticsConfigurations")
    def list_bucket_analytics_configurations(
        self,
        context: RequestContext,
        bucket: BucketName,
        continuation_token: Token | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> ListBucketAnalyticsConfigurationsOutput:
        raise NotImplementedError

    @handler("ListBucketIntelligentTieringConfigurations")
    def list_bucket_intelligent_tiering_configurations(
        self,
        context: RequestContext,
        bucket: BucketName,
        continuation_token: Token | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> ListBucketIntelligentTieringConfigurationsOutput:
        raise NotImplementedError

    @handler("ListBucketInventoryConfigurations")
    def list_bucket_inventory_configurations(
        self,
        context: RequestContext,
        bucket: BucketName,
        continuation_token: Token | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> ListBucketInventoryConfigurationsOutput:
        raise NotImplementedError

    @handler("ListBucketMetricsConfigurations")
    def list_bucket_metrics_configurations(
        self,
        context: RequestContext,
        bucket: BucketName,
        continuation_token: Token | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> ListBucketMetricsConfigurationsOutput:
        raise NotImplementedError

    @handler("ListBuckets")
    def list_buckets(
        self,
        context: RequestContext,
        max_buckets: MaxBuckets | None = None,
        continuation_token: Token | None = None,
        prefix: Prefix | None = None,
        bucket_region: BucketRegion | None = None,
        **kwargs,
    ) -> ListBucketsOutput:
        raise NotImplementedError

    @handler("ListDirectoryBuckets")
    def list_directory_buckets(
        self,
        context: RequestContext,
        continuation_token: DirectoryBucketToken | None = None,
        max_directory_buckets: MaxDirectoryBuckets | None = None,
        **kwargs,
    ) -> ListDirectoryBucketsOutput:
        raise NotImplementedError

    @handler("ListMultipartUploads")
    def list_multipart_uploads(
        self,
        context: RequestContext,
        bucket: BucketName,
        delimiter: Delimiter | None = None,
        encoding_type: EncodingType | None = None,
        key_marker: KeyMarker | None = None,
        max_uploads: MaxUploads | None = None,
        prefix: Prefix | None = None,
        upload_id_marker: UploadIdMarker | None = None,
        expected_bucket_owner: AccountId | None = None,
        request_payer: RequestPayer | None = None,
        **kwargs,
    ) -> ListMultipartUploadsOutput:
        raise NotImplementedError

    @handler("ListObjectVersions")
    def list_object_versions(
        self,
        context: RequestContext,
        bucket: BucketName,
        delimiter: Delimiter | None = None,
        encoding_type: EncodingType | None = None,
        key_marker: KeyMarker | None = None,
        max_keys: MaxKeys | None = None,
        prefix: Prefix | None = None,
        version_id_marker: VersionIdMarker | None = None,
        expected_bucket_owner: AccountId | None = None,
        request_payer: RequestPayer | None = None,
        optional_object_attributes: OptionalObjectAttributesList | None = None,
        **kwargs,
    ) -> ListObjectVersionsOutput:
        raise NotImplementedError

    @handler("ListObjects")
    def list_objects(
        self,
        context: RequestContext,
        bucket: BucketName,
        delimiter: Delimiter | None = None,
        encoding_type: EncodingType | None = None,
        marker: Marker | None = None,
        max_keys: MaxKeys | None = None,
        prefix: Prefix | None = None,
        request_payer: RequestPayer | None = None,
        expected_bucket_owner: AccountId | None = None,
        optional_object_attributes: OptionalObjectAttributesList | None = None,
        **kwargs,
    ) -> ListObjectsOutput:
        raise NotImplementedError

    @handler("ListObjectsV2")
    def list_objects_v2(
        self,
        context: RequestContext,
        bucket: BucketName,
        delimiter: Delimiter | None = None,
        encoding_type: EncodingType | None = None,
        max_keys: MaxKeys | None = None,
        prefix: Prefix | None = None,
        continuation_token: Token | None = None,
        fetch_owner: FetchOwner | None = None,
        start_after: StartAfter | None = None,
        request_payer: RequestPayer | None = None,
        expected_bucket_owner: AccountId | None = None,
        optional_object_attributes: OptionalObjectAttributesList | None = None,
        **kwargs,
    ) -> ListObjectsV2Output:
        raise NotImplementedError

    @handler("ListParts")
    def list_parts(
        self,
        context: RequestContext,
        bucket: BucketName,
        key: ObjectKey,
        upload_id: MultipartUploadId,
        max_parts: MaxParts | None = None,
        part_number_marker: PartNumberMarker | None = None,
        request_payer: RequestPayer | None = None,
        expected_bucket_owner: AccountId | None = None,
        sse_customer_algorithm: SSECustomerAlgorithm | None = None,
        sse_customer_key: SSECustomerKey | None = None,
        sse_customer_key_md5: SSECustomerKeyMD5 | None = None,
        **kwargs,
    ) -> ListPartsOutput:
        raise NotImplementedError

    @handler("PutBucketAccelerateConfiguration")
    def put_bucket_accelerate_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        accelerate_configuration: AccelerateConfiguration,
        expected_bucket_owner: AccountId | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("PutBucketAcl")
    def put_bucket_acl(
        self,
        context: RequestContext,
        bucket: BucketName,
        acl: BucketCannedACL | None = None,
        access_control_policy: AccessControlPolicy | None = None,
        content_md5: ContentMD5 | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        grant_full_control: GrantFullControl | None = None,
        grant_read: GrantRead | None = None,
        grant_read_acp: GrantReadACP | None = None,
        grant_write: GrantWrite | None = None,
        grant_write_acp: GrantWriteACP | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("PutBucketAnalyticsConfiguration")
    def put_bucket_analytics_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        id: AnalyticsId,
        analytics_configuration: AnalyticsConfiguration,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("PutBucketCors")
    def put_bucket_cors(
        self,
        context: RequestContext,
        bucket: BucketName,
        cors_configuration: CORSConfiguration,
        content_md5: ContentMD5 | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("PutBucketEncryption")
    def put_bucket_encryption(
        self,
        context: RequestContext,
        bucket: BucketName,
        server_side_encryption_configuration: ServerSideEncryptionConfiguration,
        content_md5: ContentMD5 | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("PutBucketIntelligentTieringConfiguration")
    def put_bucket_intelligent_tiering_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        id: IntelligentTieringId,
        intelligent_tiering_configuration: IntelligentTieringConfiguration,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("PutBucketInventoryConfiguration")
    def put_bucket_inventory_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        id: InventoryId,
        inventory_configuration: InventoryConfiguration,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("PutBucketLifecycle")
    def put_bucket_lifecycle(
        self,
        context: RequestContext,
        bucket: BucketName,
        content_md5: ContentMD5 | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        lifecycle_configuration: LifecycleConfiguration | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("PutBucketLifecycleConfiguration")
    def put_bucket_lifecycle_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        lifecycle_configuration: BucketLifecycleConfiguration | None = None,
        expected_bucket_owner: AccountId | None = None,
        transition_default_minimum_object_size: TransitionDefaultMinimumObjectSize | None = None,
        **kwargs,
    ) -> PutBucketLifecycleConfigurationOutput:
        raise NotImplementedError

    @handler("PutBucketLogging")
    def put_bucket_logging(
        self,
        context: RequestContext,
        bucket: BucketName,
        bucket_logging_status: BucketLoggingStatus,
        content_md5: ContentMD5 | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("PutBucketMetricsConfiguration")
    def put_bucket_metrics_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        id: MetricsId,
        metrics_configuration: MetricsConfiguration,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("PutBucketNotification")
    def put_bucket_notification(
        self,
        context: RequestContext,
        bucket: BucketName,
        notification_configuration: NotificationConfigurationDeprecated,
        content_md5: ContentMD5 | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("PutBucketNotificationConfiguration")
    def put_bucket_notification_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        notification_configuration: NotificationConfiguration,
        expected_bucket_owner: AccountId | None = None,
        skip_destination_validation: SkipValidation | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("PutBucketOwnershipControls")
    def put_bucket_ownership_controls(
        self,
        context: RequestContext,
        bucket: BucketName,
        ownership_controls: OwnershipControls,
        content_md5: ContentMD5 | None = None,
        expected_bucket_owner: AccountId | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("PutBucketPolicy")
    def put_bucket_policy(
        self,
        context: RequestContext,
        bucket: BucketName,
        policy: Policy,
        content_md5: ContentMD5 | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        confirm_remove_self_bucket_access: ConfirmRemoveSelfBucketAccess | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("PutBucketReplication")
    def put_bucket_replication(
        self,
        context: RequestContext,
        bucket: BucketName,
        replication_configuration: ReplicationConfiguration,
        content_md5: ContentMD5 | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        token: ObjectLockToken | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("PutBucketRequestPayment")
    def put_bucket_request_payment(
        self,
        context: RequestContext,
        bucket: BucketName,
        request_payment_configuration: RequestPaymentConfiguration,
        content_md5: ContentMD5 | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("PutBucketTagging")
    def put_bucket_tagging(
        self,
        context: RequestContext,
        bucket: BucketName,
        tagging: Tagging,
        content_md5: ContentMD5 | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("PutBucketVersioning")
    def put_bucket_versioning(
        self,
        context: RequestContext,
        bucket: BucketName,
        versioning_configuration: VersioningConfiguration,
        content_md5: ContentMD5 | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        mfa: MFA | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("PutBucketWebsite")
    def put_bucket_website(
        self,
        context: RequestContext,
        bucket: BucketName,
        website_configuration: WebsiteConfiguration,
        content_md5: ContentMD5 | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("PutObject")
    def put_object(
        self,
        context: RequestContext,
        bucket: BucketName,
        key: ObjectKey,
        acl: ObjectCannedACL | None = None,
        body: IO[Body] | None = None,
        cache_control: CacheControl | None = None,
        content_disposition: ContentDisposition | None = None,
        content_encoding: ContentEncoding | None = None,
        content_language: ContentLanguage | None = None,
        content_length: ContentLength | None = None,
        content_md5: ContentMD5 | None = None,
        content_type: ContentType | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        checksum_crc32: ChecksumCRC32 | None = None,
        checksum_crc32_c: ChecksumCRC32C | None = None,
        checksum_crc64_nvme: ChecksumCRC64NVME | None = None,
        checksum_sha1: ChecksumSHA1 | None = None,
        checksum_sha256: ChecksumSHA256 | None = None,
        expires: Expires | None = None,
        if_match: IfMatch | None = None,
        if_none_match: IfNoneMatch | None = None,
        grant_full_control: GrantFullControl | None = None,
        grant_read: GrantRead | None = None,
        grant_read_acp: GrantReadACP | None = None,
        grant_write_acp: GrantWriteACP | None = None,
        write_offset_bytes: WriteOffsetBytes | None = None,
        metadata: Metadata | None = None,
        server_side_encryption: ServerSideEncryption | None = None,
        storage_class: StorageClass | None = None,
        website_redirect_location: WebsiteRedirectLocation | None = None,
        sse_customer_algorithm: SSECustomerAlgorithm | None = None,
        sse_customer_key: SSECustomerKey | None = None,
        sse_customer_key_md5: SSECustomerKeyMD5 | None = None,
        ssekms_key_id: SSEKMSKeyId | None = None,
        ssekms_encryption_context: SSEKMSEncryptionContext | None = None,
        bucket_key_enabled: BucketKeyEnabled | None = None,
        request_payer: RequestPayer | None = None,
        tagging: TaggingHeader | None = None,
        object_lock_mode: ObjectLockMode | None = None,
        object_lock_retain_until_date: ObjectLockRetainUntilDate | None = None,
        object_lock_legal_hold_status: ObjectLockLegalHoldStatus | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> PutObjectOutput:
        raise NotImplementedError

    @handler("PutObjectAcl")
    def put_object_acl(
        self,
        context: RequestContext,
        bucket: BucketName,
        key: ObjectKey,
        acl: ObjectCannedACL | None = None,
        access_control_policy: AccessControlPolicy | None = None,
        content_md5: ContentMD5 | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        grant_full_control: GrantFullControl | None = None,
        grant_read: GrantRead | None = None,
        grant_read_acp: GrantReadACP | None = None,
        grant_write: GrantWrite | None = None,
        grant_write_acp: GrantWriteACP | None = None,
        request_payer: RequestPayer | None = None,
        version_id: ObjectVersionId | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> PutObjectAclOutput:
        raise NotImplementedError

    @handler("PutObjectLegalHold")
    def put_object_legal_hold(
        self,
        context: RequestContext,
        bucket: BucketName,
        key: ObjectKey,
        legal_hold: ObjectLockLegalHold | None = None,
        request_payer: RequestPayer | None = None,
        version_id: ObjectVersionId | None = None,
        content_md5: ContentMD5 | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> PutObjectLegalHoldOutput:
        raise NotImplementedError

    @handler("PutObjectLockConfiguration")
    def put_object_lock_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        object_lock_configuration: ObjectLockConfiguration | None = None,
        request_payer: RequestPayer | None = None,
        token: ObjectLockToken | None = None,
        content_md5: ContentMD5 | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> PutObjectLockConfigurationOutput:
        raise NotImplementedError

    @handler("PutObjectRetention")
    def put_object_retention(
        self,
        context: RequestContext,
        bucket: BucketName,
        key: ObjectKey,
        retention: ObjectLockRetention | None = None,
        request_payer: RequestPayer | None = None,
        version_id: ObjectVersionId | None = None,
        bypass_governance_retention: BypassGovernanceRetention | None = None,
        content_md5: ContentMD5 | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> PutObjectRetentionOutput:
        raise NotImplementedError

    @handler("PutObjectTagging")
    def put_object_tagging(
        self,
        context: RequestContext,
        bucket: BucketName,
        key: ObjectKey,
        tagging: Tagging,
        version_id: ObjectVersionId | None = None,
        content_md5: ContentMD5 | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        expected_bucket_owner: AccountId | None = None,
        request_payer: RequestPayer | None = None,
        **kwargs,
    ) -> PutObjectTaggingOutput:
        raise NotImplementedError

    @handler("PutPublicAccessBlock")
    def put_public_access_block(
        self,
        context: RequestContext,
        bucket: BucketName,
        public_access_block_configuration: PublicAccessBlockConfiguration,
        content_md5: ContentMD5 | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("RenameObject")
    def rename_object(
        self,
        context: RequestContext,
        bucket: BucketName,
        key: ObjectKey,
        rename_source: RenameSource,
        destination_if_match: IfMatch | None = None,
        destination_if_none_match: IfNoneMatch | None = None,
        destination_if_modified_since: IfModifiedSince | None = None,
        destination_if_unmodified_since: IfUnmodifiedSince | None = None,
        source_if_match: RenameSourceIfMatch | None = None,
        source_if_none_match: RenameSourceIfNoneMatch | None = None,
        source_if_modified_since: RenameSourceIfModifiedSince | None = None,
        source_if_unmodified_since: RenameSourceIfUnmodifiedSince | None = None,
        client_token: ClientToken | None = None,
        **kwargs,
    ) -> RenameObjectOutput:
        raise NotImplementedError

    @handler("RestoreObject")
    def restore_object(
        self,
        context: RequestContext,
        bucket: BucketName,
        key: ObjectKey,
        version_id: ObjectVersionId | None = None,
        restore_request: RestoreRequest | None = None,
        request_payer: RequestPayer | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> RestoreObjectOutput:
        raise NotImplementedError

    @handler("SelectObjectContent")
    def select_object_content(
        self,
        context: RequestContext,
        bucket: BucketName,
        key: ObjectKey,
        expression: Expression,
        expression_type: ExpressionType,
        input_serialization: InputSerialization,
        output_serialization: OutputSerialization,
        sse_customer_algorithm: SSECustomerAlgorithm | None = None,
        sse_customer_key: SSECustomerKey | None = None,
        sse_customer_key_md5: SSECustomerKeyMD5 | None = None,
        request_progress: RequestProgress | None = None,
        scan_range: ScanRange | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> SelectObjectContentOutput:
        raise NotImplementedError

    @handler("UpdateBucketMetadataInventoryTableConfiguration")
    def update_bucket_metadata_inventory_table_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        inventory_table_configuration: InventoryTableConfigurationUpdates,
        content_md5: ContentMD5 | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("UpdateBucketMetadataJournalTableConfiguration")
    def update_bucket_metadata_journal_table_configuration(
        self,
        context: RequestContext,
        bucket: BucketName,
        journal_table_configuration: JournalTableConfigurationUpdates,
        content_md5: ContentMD5 | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("UploadPart")
    def upload_part(
        self,
        context: RequestContext,
        bucket: BucketName,
        key: ObjectKey,
        part_number: PartNumber,
        upload_id: MultipartUploadId,
        body: IO[Body] | None = None,
        content_length: ContentLength | None = None,
        content_md5: ContentMD5 | None = None,
        checksum_algorithm: ChecksumAlgorithm | None = None,
        checksum_crc32: ChecksumCRC32 | None = None,
        checksum_crc32_c: ChecksumCRC32C | None = None,
        checksum_crc64_nvme: ChecksumCRC64NVME | None = None,
        checksum_sha1: ChecksumSHA1 | None = None,
        checksum_sha256: ChecksumSHA256 | None = None,
        sse_customer_algorithm: SSECustomerAlgorithm | None = None,
        sse_customer_key: SSECustomerKey | None = None,
        sse_customer_key_md5: SSECustomerKeyMD5 | None = None,
        request_payer: RequestPayer | None = None,
        expected_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> UploadPartOutput:
        raise NotImplementedError

    @handler("UploadPartCopy")
    def upload_part_copy(
        self,
        context: RequestContext,
        bucket: BucketName,
        copy_source: CopySource,
        key: ObjectKey,
        part_number: PartNumber,
        upload_id: MultipartUploadId,
        copy_source_if_match: CopySourceIfMatch | None = None,
        copy_source_if_modified_since: CopySourceIfModifiedSince | None = None,
        copy_source_if_none_match: CopySourceIfNoneMatch | None = None,
        copy_source_if_unmodified_since: CopySourceIfUnmodifiedSince | None = None,
        copy_source_range: CopySourceRange | None = None,
        sse_customer_algorithm: SSECustomerAlgorithm | None = None,
        sse_customer_key: SSECustomerKey | None = None,
        sse_customer_key_md5: SSECustomerKeyMD5 | None = None,
        copy_source_sse_customer_algorithm: CopySourceSSECustomerAlgorithm | None = None,
        copy_source_sse_customer_key: CopySourceSSECustomerKey | None = None,
        copy_source_sse_customer_key_md5: CopySourceSSECustomerKeyMD5 | None = None,
        request_payer: RequestPayer | None = None,
        expected_bucket_owner: AccountId | None = None,
        expected_source_bucket_owner: AccountId | None = None,
        **kwargs,
    ) -> UploadPartCopyOutput:
        raise NotImplementedError

    @handler("WriteGetObjectResponse")
    def write_get_object_response(
        self,
        context: RequestContext,
        request_route: RequestRoute,
        request_token: RequestToken,
        body: IO[Body] | None = None,
        status_code: GetObjectResponseStatusCode | None = None,
        error_code: ErrorCode | None = None,
        error_message: ErrorMessage | None = None,
        accept_ranges: AcceptRanges | None = None,
        cache_control: CacheControl | None = None,
        content_disposition: ContentDisposition | None = None,
        content_encoding: ContentEncoding | None = None,
        content_language: ContentLanguage | None = None,
        content_length: ContentLength | None = None,
        content_range: ContentRange | None = None,
        content_type: ContentType | None = None,
        checksum_crc32: ChecksumCRC32 | None = None,
        checksum_crc32_c: ChecksumCRC32C | None = None,
        checksum_crc64_nvme: ChecksumCRC64NVME | None = None,
        checksum_sha1: ChecksumSHA1 | None = None,
        checksum_sha256: ChecksumSHA256 | None = None,
        delete_marker: DeleteMarker | None = None,
        e_tag: ETag | None = None,
        expires: Expires | None = None,
        expiration: Expiration | None = None,
        last_modified: LastModified | None = None,
        missing_meta: MissingMeta | None = None,
        metadata: Metadata | None = None,
        object_lock_mode: ObjectLockMode | None = None,
        object_lock_legal_hold_status: ObjectLockLegalHoldStatus | None = None,
        object_lock_retain_until_date: ObjectLockRetainUntilDate | None = None,
        parts_count: PartsCount | None = None,
        replication_status: ReplicationStatus | None = None,
        request_charged: RequestCharged | None = None,
        restore: Restore | None = None,
        server_side_encryption: ServerSideEncryption | None = None,
        sse_customer_algorithm: SSECustomerAlgorithm | None = None,
        ssekms_key_id: SSEKMSKeyId | None = None,
        sse_customer_key_md5: SSECustomerKeyMD5 | None = None,
        storage_class: StorageClass | None = None,
        tag_count: TagCount | None = None,
        version_id: ObjectVersionId | None = None,
        bucket_key_enabled: BucketKeyEnabled | None = None,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    @handler("PostObject")
    def post_object(
        self, context: RequestContext, bucket: BucketName, body: IO[Body] | None = None, **kwargs
    ) -> PostResponse:
        raise NotImplementedError
