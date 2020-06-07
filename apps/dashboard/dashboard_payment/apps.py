from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from oscar.core.application import OscarDashboardConfig
from oscar.core.loading import get_class


class PaymentDashboardConfig(OscarDashboardConfig):
    label = 'dashboard_payment'
    name = 'apps.dashboard.dashboard_payment'
    verbose_name = _('Payment dashboard')
    namespace = 'dashboard_payment'

    default_permissions = ['is_staff', ]

    def ready(self):
        self.bankcard_create_view = get_class('dashboard.dashboard_payment.views', 'BankCardCreateView')

    def get_urls(self):
        urls = [
            # url(r'^$', self.list_view.as_view(), name='partner-list'),
            url(r'^bankcard/create/$', self.bankcard_create_view.as_view(), name='bankcard-create'),
        ]
        return self.post_process_urls(urls)
