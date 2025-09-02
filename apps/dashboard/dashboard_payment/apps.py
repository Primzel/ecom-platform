from django.urls import path
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
            path('bankcards/', self.bankcard_list_view.as_view(), name='bankcards-list'),
            path('bankcard/create/', self.bankcard_create_view.as_view(), name='bankcard-create'),
            path('bankcard/(?P<pk>\d+)/delete/', self.bankcard_delete_view.as_view(), name='bankcard-delete'),
            path('bankcard/(?P<pk>\d+)/manage/', self.bankcard_manage_view.as_view(), name='bankcard-manage'),

            path('sources/', self.source_list_view.as_view(), name='sources-list'),
            path('source/create/', self.source_create_view.as_view(), name='source-create'),
            path('source/(?P<pk>\d+)/delete/', self.source_delete_view.as_view(), name='source-delete'),
            path('source/(?P<pk>\d+)/manage/', self.source_manage_view.as_view(), name='source-manage'),

            path('source-types/', self.source_type_list_view.as_view(), name='source_types-list'),
            path('source-type/create/', self.source_type_create_view.as_view(), name='source_type-create'),
            path('source-type/(?P<pk>\d+)/delete/', self.source_type_delete_view.as_view(),
                 name='source_type-delete'),
            path('source-type/(?P<pk>\d+)/manage/', self.source_type_manage_view.as_view(),
                 name='source_type-manage'),

            path('transactions/', self.transaction_list_view.as_view(), name='transactions-list'),
            path('transaction/create/', self.transaction_create_view.as_view(), name='transaction-create'),
            path('transaction/(?P<pk>\d+)/delete/', self.transaction_delete_view.as_view(),
                 name='transaction-delete'),
            path('transaction/(?P<pk>\d+)/manage/', self.transaction_manage_view.as_view(),
                 name='transaction-manage'),

            path('payment-methods/', self.payment_method_list_view.as_view(), name='payment_methods-list'),
            path('payment-method/create/', self.payment_method_create_view.as_view(), name='payment_method-create'),
            path('payment-method/(?P<pk>\d+)/delete/', self.payment_method_delete_view.as_view(),
                 name='payment_method-delete'),
            path('payment-method/(?P<pk>\d+)/manage/', self.payment_method_manage_view.as_view(),
                 name='payment_method-manage'),

            path('payment-gateways/', self.payment_gateway_list_view.as_view(), name='payment_gateways-list'),
            path('payment-gateway/create/', self.payment_gateway_create_view.as_view(),
                 name='payment_gateway-create'),
            path('payment-gateway/(?P<pk>\d+)/delete/', self.payment_gateway_delete_view.as_view(),
                 name='payment_gateway-delete'),
            path('payment-gateway/(?P<pk>\d+)/manage/', self.payment_gateway_manage_view.as_view(),
                 name='payment_gateway-manage'),
        ]
        return self.post_process_urls(urls)
