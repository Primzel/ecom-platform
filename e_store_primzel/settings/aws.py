import os

THUMBNAIL_DEBUG = False
THUMBNAIL_PRESERVE_FORMAT = True

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '123')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'xyz')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME', 'demo-bucket')
AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL', 'http://com.localstack.s3:4566/')
AWS_S3_USE_SSL = os.getenv('AWS_S3_USE_SSL', False)
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
DEFAULT_FILE_STORAGE = 'backends.storage_backends.MediaStorage'
AWS_S3_SECURE_URLS = os.getenv('AWS_S3_SECURE_URLS', False)
AWS_PRELOAD_METADATA = os.getenv('AWS_PRELOAD_METADATA', False)
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-east-2')

AWS_SES_REGION_NAME = os.getenv('AWS_SES_REGION_NAME', 'us-east-2')
AWS_SES_REGION_ENDPOINT = os.getenv('AWS_SES_REGION_ENDPOINT', 'email.us-east-2.amazonaws.com')
STATICFILES_STORAGE = "backends.storage_backends.StaticFileStorage"

# # Static files settings
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATIC_URL = f'{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/'

AWS_QUERYSTRING_AUTH = os.getenv('AWS_QUERYSTRING_AUTH', False)
AWS_S3_SIGNATURE_VERSION = os.getenv('AWS_S3_SIGNATURE_VERSION', 's3v4')
