from oscar.core.application import OscarDashboardConfig
from django.utils.translation import gettext_lazy as _

class SettingsConfig(OscarDashboardConfig):
    name = 'settings'
    verbose_name = _('Settings')
    namespace = 'settings'
    default_permissions = ['is_staff']

    def ready(self):
        pass

    def get_urls(self):
        urls = [

        ]
        return self.post_process_urls(urls)
