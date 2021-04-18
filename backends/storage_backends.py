import logging

from django.db import connection
from storages.backends.s3boto3 import S3Boto3Storage
from storages.utils import setting
from multitenancy.models import Tenant

log = logging.getLogger(__name__)


class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
    tenants = {}

    def __init__(self, **settings):
        super().__init__(**settings)

    def get_default_settings(self):
        settings = super(MediaStorage, self).get_default_settings()
        settings.update([{'bucket_name', self.tenant_bucket_name}])
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
        log.debug(f'Using {bucket_name} for tenant {self.tenant.schema_name}')
        return bucket_name

    @property
    def bucket(self):
        return self.connection.Bucket(self.tenant_bucket_name)
