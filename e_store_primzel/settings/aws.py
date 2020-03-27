AWS_ACCESS_KEY_ID = '123'
AWS_SECRET_ACCESS_KEY = 'xyz'
AWS_STORAGE_BUCKET_NAME = 'demo-bucket'
AWS_S3_ENDPOINT_URL = 'http://localhost:4572'
AWS_S3_CUSTOM_DOMAIN = '%s.localhost:4572' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

DEFAULT_FILE_STORAGE = 'backends.storage_backends.MediaStorage'
MEDIA_URL='/demo-bucket/media/'