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
        self.bankcard_list_view = get_class('dashboard.dashboard_payment.views', 'BankCardListView')
        self.bankcard_delete_view = get_class('dashboard.dashboard_payment.views', 'BankCardDeleteView')
        self.bankcard_manage_view = get_class('dashboard.dashboard_payment.views', 'BankCardManageView')

    def get_urls(self):
        urls = [
            url(r'^$', self.bankcard_list_view.as_view(), name='bankcards-list'),
            url(r'^bankcard/create/$', self.bankcard_create_view.as_view(), name='bankcard-create'),
            url(r'^bankcard/(?P<pk>\d+)/delete/$', self.bankcard_delete_view.as_view(), name='bankcard-delete'),
            url(r'^bankcard/(?P<pk>\d+)/manage/$', self.bankcard_manage_view.as_view(), name='bankcard-manage'),
        ]
        return self.post_process_urls(urls)
