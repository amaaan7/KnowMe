from storages.backends.s3boto3 import S3Boto3Storage

class PublicMediaStorage(S3Boto3Storage):
    """
    Custom storage class that makes uploaded files publicly accessible.
    """
    default_acl = 'public-read'
    file_overwrite = False

