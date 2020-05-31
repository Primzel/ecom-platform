from django.db import models
from django.utils.translation import gettext_lazy as _

from oscar.apps.payment.models import *  # noqa isort:skip


class PaymentMethod(models.Model):
    title = models.CharField(max_length=255)
    payment_gateway = models.ForeignKey('payment_gateways.AvailablePaymentGateway', on_delete=models.DO_NOTHING,
                                        related_name='integrations')
    publishable_key = models.CharField(max_length=1024, blank=False, null=False, help_text=_('Publishable key'))
    secret_key = models.CharField(max_length=1024, blank=False, null=False, help_text=_('Secret key'))
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title
