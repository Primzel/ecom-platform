from django.contrib import admin

# Register your models here.
from primzel.payment_gateways.models import AvailablePaymentGateway

admin.site.register(AvailablePaymentGateway)
