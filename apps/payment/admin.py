from oscar.apps.payment.admin import *  # noqa

from apps.payment.models import PaymentMethod

admin.site.register(PaymentMethod)
