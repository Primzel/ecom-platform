  
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from oscar.core.compat import get_user_model
from oscar.core.loading import get_model, get_class

User = get_user_model()
Bankcard = get_model('payment', 'Bankcard')
Source = get_model('payment', 'Source')
SourceType = get_model('payment', 'SourceType')
Transaction = get_model('payment', 'Transaction')
PaymentMethod = get_model('payment', 'PaymentMethod')
AvailablePaymentGateway = get_model('payment_gateways', 'AvailablePaymentGateway')


BankCardForm = get_class('dashboard.dashboard_payment.forms', 'BankCardForm')
SourceForm = get_class('dashboard.dashboard_payment.forms', 'SourceForm')
SourceTypeForm = get_class('dashboard.dashboard_payment.forms', 'SourceTypeForm')
TransactionForm = get_class('dashboard.dashboard_payment.forms', 'TransactionForm')
PaymentMethodForm = get_class('dashboard.dashboard_payment.forms', 'PaymentMethodForm')
AvailablePaymentGatewayForm = get_class('dashboard.dashboard_payment.forms', 'AvailablePaymentGatewayForm')


class BankCardCreateView(generic.CreateView):
    model = Bankcard
    template_name = 'oscar/dashboad/payment/payment_form.html'
    form_class = BankCardForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = _('Add a new bank card')
        return ctx

    def get_success_url(self):
        messages.success(self.request, _("Bank card '%s' was added successfully.") % self.object.name)
        return reverse('dashboard:dashboard_payment:bankcards-list')


class BankCardListView(generic.ListView):
    model = Bankcard
    context_object_name = 'bankcards'
    template_name = 'oscar/dashboad/payment/bankcard/bankcards_list.html'
    queryset = Bankcard.objects.all()

    def get_queryset(self, **kwargs):
        qs = super(BankCardListView, self).get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super(BankCardListView, self).get_context_data(**kwargs)
        ctx['title'] = _("Bank Cards")
        ctx['create_new_object_url'] = reverse('dashboard:dashboard_payment:bankcard-create')
        return ctx


class BankCardDeleteView(generic.DeleteView):
    model = Bankcard
    context_object_name = 'object'
    template_name = 'oscar/dashboad/payment/payment_delete.html'

    def get_success_url(self):
        messages.success(self.request, _("Bank card '%s' was deleted successfully.") % self.object.name)
        return reverse('dashboard:dashboard_payment:bankcards-list')

    def get_context_data(self, **kwargs):
        ctx = super(BankCardDeleteView, self).get_context_data(**kwargs)
        ctx['title'] = _("Bank Card")
        ctx['object_listing_url'] = reverse('dashboard:dashboard_payment:bankcards-list')
        ctx['object_manage_url'] = reverse('dashboard:dashboard_payment:bankcard-manage',  kwargs={'pk': self.object.pk})
        ctx['object_name'] = _(self.object.name)
        return ctx


class BankCardManageView(generic.UpdateView):
    model = Bankcard
    context_object_name = 'bankcard'
    template_name = 'oscar/dashboad/payment/payment_manage.html'
    form_class = BankCardForm
    success_url = reverse_lazy('dashboard:dashboard_payment:bankcards-list')

    def get_context_data(self, **kwargs):
        ctx = super(BankCardManageView, self).get_context_data(**kwargs)
        ctx['title'] = _("Bank Card")
        ctx['object_listing_url'] = reverse('dashboard:dashboard_payment:bankcards-list')
        ctx['object_name'] = _(self.object.name)
        return ctx

    def form_valid(self, form):
        messages.success(self.request, _("Bank card '%s' was updated successfully.") % self.object.name)
        self.object.save()
        return super().form_valid(form)


class SourceCreateView(generic.CreateView):
    model = Source
    template_name = 'oscar/dashboad/payment/payment_form.html'
    form_class = SourceForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = _('Add a new source')
        return ctx

    def get_success_url(self):
        messages.success(self.request, _("Source '%s' was added successfully.") % self.object.order.number)
        return reverse('dashboard:dashboard_payment:sources-list')


class SourceListView(generic.ListView):
    model = Source
    context_object_name = 'sources'
    template_name = 'oscar/dashboad/payment/source/sources_list.html'
    queryset = Source.objects.all()

    def get_queryset(self, **kwargs):
        qs = super(SourceListView, self).get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super(SourceListView, self).get_context_data(**kwargs)
        ctx['title'] = _("Sources")
        ctx['create_new_object_url'] = reverse('dashboard:dashboard_payment:source-create')
        return ctx


class SourceDeleteView(generic.DeleteView):
    model = Source
    context_object_name = 'object'
    template_name = 'oscar/dashboad/payment/payment_delete.html'

    def get_success_url(self):
        messages.success(self.request, _("Source '%s' was deleted successfully.") % self.object.order.number)
        return reverse('dashboard:dashboard_payment:sources-list')

    def get_context_data(self, **kwargs):
        ctx = super(SourceDeleteView, self).get_context_data(**kwargs)
        ctx['title'] = _("Source")
        ctx['object_listing_url'] = reverse('dashboard:dashboard_payment:sources-list')
        ctx['object_manage_url'] = reverse('dashboard:dashboard_payment:source-manage', kwargs={'pk': self.object.pk})
        ctx['object_name'] = _(self.object.order.number)
        return ctx


class SourceManageView(generic.UpdateView):
    model = Source
    context_object_name = 'source'
    template_name = 'oscar/dashboad/payment/payment_manage.html'
    form_class = SourceForm
    success_url = reverse_lazy('dashboard:dashboard_payment:sources-list')

    def get_context_data(self, **kwargs):
        ctx = super(SourceManageView, self).get_context_data(**kwargs)
        ctx['title'] = _("Source")
        ctx['object_listing_url'] = reverse('dashboard:dashboard_payment:sources-list')
        ctx['object_name'] = _(self.object.order.number)
        return ctx

    def form_valid(self, form):
        messages.success(self.request, _("Sources '%s' was updated successfully.") % self.object.order.number)
        self.object.save()
        return super().form_valid(form)


class SourceTypeCreateView(generic.CreateView):
    model = SourceType
    template_name = 'oscar/dashboad/payment/payment_form.html'
    form_class = SourceTypeForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = _('Add a new source type')
        return ctx

    def get_success_url(self):
        messages.success(self.request, _("Source type '%s' was added successfully.") % self.object.name)
        return reverse('dashboard:dashboard_payment:source_types-list')


class SourceTypeListView(generic.ListView):
    model = SourceType
    context_object_name = 'source_types'
    template_name = 'oscar/dashboad/payment/source_types/source_types_list.html'
    queryset = SourceType.objects.all()

    def get_queryset(self, **kwargs):
        qs = super(SourceTypeListView, self).get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super(SourceTypeListView, self).get_context_data(**kwargs)
        ctx['title'] = _("Source Types")
        ctx['create_new_object_url'] = reverse('dashboard:dashboard_payment:source_type-create')
        return ctx


class SourceTypeDeleteView(generic.DeleteView):
    model = SourceType
    context_object_name = 'object'
    template_name = 'oscar/dashboad/payment/payment_delete.html'

    def get_success_url(self):
        messages.success(self.request, _("Source type '%s' was deleted successfully.") % self.object.name)
        return reverse('dashboard:dashboard_payment:source_types-list')

    def get_context_data(self, **kwargs):
        ctx = super(SourceTypeDeleteView, self).get_context_data(**kwargs)
        ctx['title'] = _("Source Type")
        ctx['object_listing_url'] = reverse('dashboard:dashboard_payment:source_types-list')
        ctx['object_manage_url'] = reverse('dashboard:dashboard_payment:source_type-manage', kwargs={'pk': self.object.pk})
        ctx['object_name'] = _(self.object.name)
        return ctx


class SourceTypeManageView(generic.UpdateView):
    model = SourceType
    context_object_name = 'source_type'
    template_name = 'oscar/dashboad/payment/payment_manage.html'
    form_class = SourceTypeForm
    success_url = reverse_lazy('dashboard:dashboard_payment:source_types-list')

    def get_context_data(self, **kwargs):
        ctx = super(SourceTypeManageView, self).get_context_data(**kwargs)
        ctx['title'] = _("Source Type")
        ctx['object_listing_url'] = reverse('dashboard:dashboard_payment:source_types-list')
        ctx['object_name'] = _(self.object.name)
        return ctx

    def form_valid(self, form):
        messages.success(self.request, _("Source Type '%s' was updated successfully.") % self.object.name)
        self.object.save()
        return super().form_valid(form)


class TransactionCreateView(generic.CreateView):
    model = Transaction
    template_name = 'oscar/dashboad/payment/payment_form.html'
    form_class = TransactionForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = _('Add a transaction')
        return ctx

    def get_success_url(self):
        messages.success(self.request, _("Transaction was added successfully."))
        return reverse('dashboard:dashboard_payment:transactions-list')


class TransactionsListView(generic.ListView):
    model = Transaction
    context_object_name = 'transactions'
    template_name = 'oscar/dashboad/payment/transactions/transactions_list.html'
    queryset = Transaction.objects.all()

    def get_queryset(self, **kwargs):
        qs = super(TransactionsListView, self).get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super(TransactionsListView, self).get_context_data(**kwargs)
        ctx['title'] = _("Transactions")
        ctx['create_new_object_url'] = reverse('dashboard:dashboard_payment:transaction-create')
        return ctx


class TransactionDeleteView(generic.DeleteView):
    model = Transaction
    context_object_name = 'object'
    template_name = 'oscar/dashboad/payment/payment_delete.html'

    def get_success_url(self):
        messages.success(self.request, _("Transaction was deleted successfully."))
        return reverse('dashboard:dashboard_payment:transactions-list')

    def get_context_data(self, **kwargs):
        ctx = super(TransactionDeleteView, self).get_context_data(**kwargs)
        ctx['title'] = _("Transaction")
        ctx['object_listing_url'] = reverse('dashboard:dashboard_payment:transactions-list')
        ctx['object_manage_url'] = reverse('dashboard:dashboard_payment:transaction-manage', kwargs={'pk': self.object.pk})
        ctx['object_name'] = _(self.object.amount)
        return ctx


class TransactionManageView(generic.UpdateView):
    model = Transaction
    context_object_name = 'transaction'
    template_name = 'oscar/dashboad/payment/payment_manage.html'
    form_class = TransactionForm
    success_url = reverse_lazy('dashboard:dashboard_payment:transactions-list')

    def get_context_data(self, **kwargs):
        ctx = super(TransactionManageView, self).get_context_data(**kwargs)
        ctx['title'] = _("Transaction")
        ctx['object_listing_url'] = reverse('dashboard:dashboard_payment:transactions-list')
        ctx['object_name'] = _(self.object.amount)
        return ctx

    def form_valid(self, form):
        messages.success(self.request, _("Transaction '%s' was updated successfully.") % self.object.amount)
        self.object.save()
        return super().form_valid(form)


class PaymentMethodCreateView(generic.CreateView):
    model = PaymentMethod
    template_name = 'oscar/dashboad/payment/payment_form.html'
    form_class = PaymentMethodForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = _('Add a payment method')
        return ctx

    def get_success_url(self):
        messages.success(self.request, _("Payment method '%s' was added successfully.") % self.object.title)
        return reverse('dashboard:dashboard_payment:payment_methods-list')


class PaymentMethodListView(generic.ListView):
    model = PaymentMethod
    context_object_name = 'payment_methods'
    template_name = 'oscar/dashboad/payment/payment_methods/payment_methods_list.html'
    queryset = PaymentMethod.objects.all()

    def get_queryset(self, **kwargs):
        qs = super(PaymentMethodListView, self).get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super(PaymentMethodListView, self).get_context_data(**kwargs)
        ctx['title'] = _("Payment Methods")
        ctx['create_new_object_url'] = reverse('dashboard:dashboard_payment:payment_method-create')
        return ctx


class PaymentMethodDeleteView(generic.DeleteView):
    model = PaymentMethod
    context_object_name = 'object'
    template_name = 'oscar/dashboad/payment/payment_delete.html'

    def get_success_url(self):
        messages.success(self.request, _("Transaction %s was deleted successfully.") % self.object.title)
        return reverse('dashboard:dashboard_payment:payment_methods-list')

    def get_context_data(self, **kwargs):
        ctx = super(PaymentMethodDeleteView, self).get_context_data(**kwargs)
        ctx['title'] = _("Payment Method")
        ctx['object_listing_url'] = reverse('dashboard:dashboard_payment:payment_methods-list')
        ctx['object_manage_url'] = reverse('dashboard:dashboard_payment:payment_method-manage', kwargs={'pk': self.object.pk})
        ctx['object_name'] = _(self.object.title)
        return ctx


class PaymentMethodManageView(generic.UpdateView):
    model = PaymentMethod
    context_object_name = 'payment_method'
    template_name = 'oscar/dashboad/payment/payment_manage.html'
    form_class = PaymentMethodForm
    success_url = reverse_lazy('dashboard:dashboard_payment:payment_methods-list')

    def get_context_data(self, **kwargs):
        ctx = super(PaymentMethodManageView, self).get_context_data(**kwargs)
        ctx['title'] = _("Payment Method")
        ctx['object_listing_url'] = reverse('dashboard:dashboard_payment:payment_methods-list')
        ctx['object_name'] = _(self.object.title)
        return ctx

    def form_valid(self, form):
        messages.success(self.request, _("Payment Method '%s' was updated successfully.") % self.object.title)
        self.object.save()
        return super().form_valid(form)


class AvailablePaymentGatewayCreateView(generic.CreateView):
    model = AvailablePaymentGateway
    template_name = 'oscar/dashboad/payment/payment_form.html'
    form_class = AvailablePaymentGatewayForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = _('Add a payment gateway')
        return ctx

    def get_success_url(self):
        messages.success(self.request, _("Payment gateway '%s' was added successfully.") % self.object.name)
        return reverse('dashboard:dashboard_payment:payment_gateways-list')


class AvailablePaymentGatewayListView(generic.ListView):
    model = AvailablePaymentGateway
    context_object_name = 'payment_gateways'
    template_name = 'oscar/dashboad/payment/payment_gateways/payment_gateways_list.html'
    queryset = AvailablePaymentGateway.objects.all()

    def get_queryset(self, **kwargs):
        qs = super(AvailablePaymentGatewayListView, self).get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super(AvailablePaymentGatewayListView, self).get_context_data(**kwargs)
        ctx['title'] = _("Payment Gateways")
        ctx['create_new_object_url'] = reverse('dashboard:dashboard_payment:payment_gateway-create')
        return ctx


class AvailablePaymentGatewayDeleteView(generic.DeleteView):
    model = AvailablePaymentGateway
    context_object_name = 'object'
    template_name = 'oscar/dashboad/payment/payment_delete.html'

    def get_success_url(self):
        messages.success(self.request, _("Payment gateway %s was deleted successfully.") % self.object.name)
        return reverse('dashboard:dashboard_payment:payment_gateways-list')

    def get_context_data(self, **kwargs):
        ctx = super(AvailablePaymentGatewayDeleteView, self).get_context_data(**kwargs)
        ctx['title'] = _("Payment Gateway")
        ctx['object_listing_url'] = reverse('dashboard:dashboard_payment:payment_gateways-list')
        ctx['object_manage_url'] = reverse('dashboard:dashboard_payment:payment_gateway-manage', kwargs={'pk': self.object.pk})
        ctx['object_name'] = _(self.object.name)
        return ctx


class AvailablePaymentGatewayManageView(generic.UpdateView):
    model = AvailablePaymentGateway
    context_object_name = 'payment_gateway'
    template_name = 'oscar/dashboad/payment/payment_manage.html'
    form_class = AvailablePaymentGatewayForm
    success_url = reverse_lazy('dashboard:dashboard_payment:payment_gateways-list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = _("Payment Gateway")
        ctx['object_listing_url'] = reverse('dashboard:dashboard_payment:payment_gateways-list')
        ctx['object_name'] = _(self.object.name)
        return ctx

    def form_valid(self, form):
        messages.success(self.request, _("Payment gateway '%s' was updated successfully.") % self.object.name)
        self.object.save()
        return super().form_valid(form)
