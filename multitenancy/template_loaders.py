"""
Template loaders.
"""
import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import connection
from django_tenants.template.loaders.filesystem import Loader
from django_tenants.staticfiles.finders import TenantFileSystemFinder

from multitenancy.models import Tenant


def parse_tenant_config_path(config_path, template_dir_name):
    """
    Convenience function for parsing django-tenants' path configuration strings.

    If the string contains '%s', then the current tenant's schema name will be inserted at that location. Otherwise
    the schema name will be appended to the end of the string.

    :param config_path: A configuration path string that optionally contains '%s' to indicate where the tenant
    schema name should be inserted.

    :return: The formatted string containing the schema name
    """
    try:
        # Insert schema name
        return config_path % template_dir_name
    except (TypeError, ValueError):
        # No %s in string; append schema name at the end
        return os.path.join(config_path, template_dir_name)


class PrimzelTemplateLoader(Loader):
    @property
    def dirs(self):
        """
        Lazy retrieval of list of template directories based on current tenant schema.
        :return: The list of template file dirs that have been configured for this tenant.
        """
        if self._dirs.get(connection.schema_name, None) is None:
            try:
                # Use directories configured via MULTITENANT_TEMPLATE_DIRS
                dirs = [
                    parse_tenant_config_path(dir_, self.template_dir)
                    for dir_ in settings.MULTITENANT_TEMPLATE_DIRS
                ]
            except AttributeError:
                raise ImproperlyConfigured(
                    "To use {}.{} you must define the MULTITENANT_TEMPLATE_DIRS setting.".format(
                        __name__, Loader.__name__
                    )
                )

            self.dirs = dirs

        return self._dirs[connection.schema_name]

    @dirs.setter
    def dirs(self, value):
        self._dirs[connection.schema_name] = value

    @property
    def template_dir(self):
        return Tenant.objects.get(schema_name=connection.schema_name).template_dir_name


class PrimzelStaticFileLoader(TenantFileSystemFinder):

    @property
    def locations(self):
        """
        Lazy retrieval of list of locations with static files based on current tenant schema.
        :return: The list of static file dirs that have been configured for this tenant.
        """
        if self._locations.get(connection.schema_name, None) is None:
            schema_locations = []
            for root in settings.MULTITENANT_STATICFILES_DIRS:
                root = parse_tenant_config_path(root, self.template_dir)

                if isinstance(root, (list, tuple)):
                    prefix, root = root
                else:
                    prefix = ""

                if (prefix, root) not in schema_locations:
                    schema_locations.append((prefix, root))

            self._locations[connection.schema_name] = schema_locations

        return self._locations[connection.schema_name]

    @property
    def template_dir(self):
        try:
            template_dir = Tenant.objects.get(schema_name=connection.schema_name).template_dir_name
        except Exception as ex:
            template_dir = ''
        return template_dir
