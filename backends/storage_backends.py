import logging

from django.contrib.staticfiles.storage import ManifestFilesMixin
from django.db import connection
from storages.backends.s3boto3 import S3Boto3Storage
from storages.utils import setting

from multitenancy.models import Tenant

log = logging.getLogger('primzel.logger')


class MediaStorage(S3Boto3Storage):
    file_overwrite = False
    secure_urls = False
    tenants = {}

    def __init__(self, **settings):
        super().__init__(**settings)

    def get_default_settings(self):
        settings = super(MediaStorage, self).get_default_settings()
        settings.update({'bucket_name': self.tenant_bucket_name})
        return settings

    @property
    def tenant(self):
        tenant = self.tenants.get(connection.schema_name, None)
        try:
            if not tenant:
                self.tenants[connection.schema_name] = tenant = Tenant.objects.get(schema_name=connection.schema_name)
        except Exception as ex:
            log.exception('Unable to get tenant', ex)
        return tenant

    @property
    def tenant_bucket_name(self):
        bucket_name = self.tenant.s3_bucket_name if self.tenant else setting('AWS_STORAGE_BUCKET_NAME')
        return bucket_name

    @property
    def bucket(self):
        return self.connection.Bucket(self.tenant_bucket_name)

    @property
    def location(self):
        return self.tenant.name


class StaticFileStorage(ManifestFilesMixin, MediaStorage):
    file_overwrite = True
    manifest_strict = False
    secure_urls = False

    def get_default_settings(self):
        settings = super(StaticFileStorage, self).get_default_settings()
        return settings
