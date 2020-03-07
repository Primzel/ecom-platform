from django.utils.deprecation import MiddlewareMixin
from django_tenant_templates import local
from django_tenant_templates.middleware import TenantMiddleware


class TenantTemplatesMiddleware(TenantMiddleware, MiddlewareMixin):
    def process_request(self, request):
        request.tenant_slug = request.tenant.name
        local.tenant_slug = getattr(request, self.slug_property_name, None)
