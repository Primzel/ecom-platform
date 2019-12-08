from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ConfigurableMenuConfig(AppConfig):
    name = 'apps.dashboard.configurable_menu'
    label = 'configurable_menu'
    verbose_name = _('Configurable Menu')
    default_permissions = ['is_staff', ]
    def ready(self):
        pass

    def get_urls(self):
        urls = [

        ]
        return self.post_process_urls(urls)
