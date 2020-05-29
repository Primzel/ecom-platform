from django.conf import settings

from apps.dashboard.settings.models import Setting


def store(request):
    setting = Setting.objects.filter(is_active=True).order_by('id').first()
    kwargs = {
        'setting': setting
    }
    return kwargs
