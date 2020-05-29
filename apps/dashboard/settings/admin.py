from django.contrib import admin

# Register your models here.
from apps.dashboard.settings.models import Setting

admin.site.register(Setting)
