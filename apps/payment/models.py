from django.db import models
from django.utils.translation import gettext_lazy as _

from oscar.apps.payment.models import *  # noqa isort:skip
from oscar.core.utils import get_default_currency


class PaymentMethod(models.Model):
    title = models.CharField(max_length=255)
    payment_gateway = models.ForeignKey('payment_gateways.AvailablePaymentGateway', on_delete=models.DO_NOTHING,
                                        related_name='integrations')
    publishable_key = models.CharField(max_length=1024, blank=False, null=False, help_text=_('Publishable key'))
    secret_key = models.CharField(max_length=1024, blank=False, null=False, help_text=_('Secret key'))
    price_currency = models.CharField(
        _("Currency"), max_length=12, default=get_default_currency)
    currency_factory = models.IntegerField(default=1,
                                           help_text=_('1 Dollar = 100 cents (1 dollar x Currency Factor(100) = 100)'),
                                           verbose_name=_('Currency Factor'))
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title
