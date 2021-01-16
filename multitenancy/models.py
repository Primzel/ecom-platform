from django.db import models

# Create your models here.
from django_tenants.models import TenantMixin, DomainMixin


class Tenant(TenantMixin):
    name = models.CharField(max_length=100)
    template_dir_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    paid_until = models.DateField()
    on_trial = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)


class Domain(DomainMixin):
    pass
