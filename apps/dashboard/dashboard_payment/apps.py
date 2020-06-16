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

        self.source_create_view = get_class('dashboard.dashboard_payment.views', 'SourceCreateView')
        self.source_list_view = get_class('dashboard.dashboard_payment.views', 'SourceListView')
        self.source_delete_view = get_class('dashboard.dashboard_payment.views', 'SourceDeleteView')
        self.source_manage_view = get_class('dashboard.dashboard_payment.views', 'SourceManageView')

        self.source_type_create_view = get_class('dashboard.dashboard_payment.views', 'SourceTypeCreateView')
        self.source_type_list_view = get_class('dashboard.dashboard_payment.views', 'SourceTypeListView')
        self.source_type_delete_view = get_class('dashboard.dashboard_payment.views', 'SourceTypeDeleteView')
        self.source_type_manage_view = get_class('dashboard.dashboard_payment.views', 'SourceTypeManageView')

        self.transaction_create_view = get_class('dashboard.dashboard_payment.views', 'TransactionCreateView')
        self.transaction_list_view = get_class('dashboard.dashboard_payment.views', 'TransactionsListView')
        self.transaction_delete_view = get_class('dashboard.dashboard_payment.views', 'TransactionDeleteView')
        self.transaction_manage_view = get_class('dashboard.dashboard_payment.views', 'TransactionManageView')

        self.payment_method_create_view = get_class('dashboard.dashboard_payment.views', 'PaymentMethodCreateView')
        self.payment_method_list_view = get_class('dashboard.dashboard_payment.views', 'PaymentMethodListView')
        self.payment_method_delete_view = get_class('dashboard.dashboard_payment.views', 'PaymentMethodDeleteView')
        self.payment_method_manage_view = get_class('dashboard.dashboard_payment.views', 'PaymentMethodManageView')

        self.payment_gateway_create_view = get_class('dashboard.dashboard_payment.views', 'AvailablePaymentGatewayCreateView')
        self.payment_gateway_list_view = get_class('dashboard.dashboard_payment.views', 'AvailablePaymentGatewayListView')
        self.payment_gateway_delete_view = get_class('dashboard.dashboard_payment.views', 'AvailablePaymentGatewayDeleteView')
        self.payment_gateway_manage_view = get_class('dashboard.dashboard_payment.views', 'AvailablePaymentGatewayManageView')

    def get_urls(self):
        urls = [
            url(r'^bankcards/$', self.bankcard_list_view.as_view(), name='bankcards-list'),
            url(r'^bankcard/create/$', self.bankcard_create_view.as_view(), name='bankcard-create'),
            url(r'^bankcard/(?P<pk>\d+)/delete/$', self.bankcard_delete_view.as_view(), name='bankcard-delete'),
            url(r'^bankcard/(?P<pk>\d+)/manage/$', self.bankcard_manage_view.as_view(), name='bankcard-manage'),

            url(r'^sources/$', self.source_list_view.as_view(), name='sources-list'),
            url(r'^source/create/$', self.source_create_view.as_view(), name='source-create'),
            url(r'^source/(?P<pk>\d+)/delete/$', self.source_delete_view.as_view(), name='source-delete'),
            url(r'^source/(?P<pk>\d+)/manage/$', self.source_manage_view.as_view(), name='source-manage'),

            url(r'^source-types/$', self.source_type_list_view.as_view(), name='source_types-list'),
            url(r'^source-type/create/$', self.source_type_create_view.as_view(), name='source_type-create'),
            url(r'^source-type/(?P<pk>\d+)/delete/$', self.source_type_delete_view.as_view(), name='source_type-delete'),
            url(r'^source-type/(?P<pk>\d+)/manage/$', self.source_type_manage_view.as_view(), name='source_type-manage'),

            url(r'^transactions/$', self.transaction_list_view.as_view(), name='transactions-list'),
            url(r'^transaction/create/$', self.transaction_create_view.as_view(), name='transaction-create'),
            url(r'^transaction/(?P<pk>\d+)/delete/$', self.transaction_delete_view.as_view(), name='transaction-delete'),
            url(r'^transaction/(?P<pk>\d+)/manage/$', self.transaction_manage_view.as_view(), name='transaction-manage'),

            url(r'^payment-methods/$', self.payment_method_list_view.as_view(), name='payment_methods-list'),
            url(r'^payment-method/create/$', self.payment_method_create_view.as_view(), name='payment_method-create'),
            url(r'^payment-method/(?P<pk>\d+)/delete/$', self.payment_method_delete_view.as_view(), name='payment_method-delete'),
            url(r'^payment-method/(?P<pk>\d+)/manage/$', self.payment_method_manage_view.as_view(), name='payment_method-manage'),

            url(r'^payment-gateways/$', self.payment_gateway_list_view.as_view(), name='payment_gateways-list'),
            url(r'^payment-gateway/create/$', self.payment_gateway_create_view.as_view(), name='payment_gateway-create'),
            url(r'^payment-gateway/(?P<pk>\d+)/delete/$', self.payment_gateway_delete_view.as_view(), name='payment_gateway-delete'),
            url(r'^payment-gateway/(?P<pk>\d+)/manage/$', self.payment_gateway_manage_view.as_view(), name='payment_gateway-manage'),
        ]
        return self.post_process_urls(urls)
