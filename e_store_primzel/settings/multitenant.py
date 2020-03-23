import os

from django.conf.global_settings import STATICFILES_FINDERS
from .base import BASE_DIR

TENANT_MODEL = "multitenancy.Tenant"
TENANT_DOMAIN_MODEL = "multitenancy.Domain"

STATICFILES_FINDERS.insert(0, "django_tenants.staticfiles.finders.TenantFileSystemFinder")

MULTITENANT_STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "templates/%s/static"),
]

STATICFILES_STORAGE = "django_tenants.staticfiles.storage.TenantStaticFilesStorage"
MULTITENANT_RELATIVE_STATIC_ROOT = ""  # (default: create sub-directory for each tenant)
DEFAULT_FILE_STORAGE = "django_tenants.files.storage.TenantFileSystemStorage"
