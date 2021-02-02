from django.conf import settings

from apps.dashboard.settings.models import Setting
from apps.payment.models import PaymentMethod


def store(request):
    setting = Setting.effective_settings.get()
    payment_methods = PaymentMethod.objects.filter(is_active=True)
    kwargs = {
        'setting': setting,
        'payment_methods': payment_methods
    }
    return kwargs
