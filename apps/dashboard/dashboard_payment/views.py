  
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from oscar.core.compat import get_user_model
from oscar.core.loading import get_model, get_class

User = get_user_model()
Bankcard = get_model('payment', 'Bankcard')
BankCardForm = get_class('dashboard.dashboard_payment.forms', 'BankCardForm')


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
    template_name = 'oscar/dashboad/payment/payment_list.html'
    queryset = Bankcard.objects.all()

    def get_queryset(self, **kwargs):
        qs = super(BankCardListView, self).get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super(BankCardListView, self).get_context_data(**kwargs)
        ctx['title'] = _("Bank Cards")
        return ctx


class BankCardDeleteView(generic.DeleteView):
    model = Bankcard
    context_object_name = 'bankcard'
    template_name = 'oscar/dashboad/payment/payment_delete.html'

    def get_success_url(self):
        messages.success(self.request, _("Bank card '%s' was deleted successfully.") % self.object.name)
        return reverse('dashboard:dashboard_payment:bankcards-list')


class BankCardManageView(generic.UpdateView):
    model = Bankcard
    context_object_name = 'bankcard'
    template_name = 'oscar/dashboad/payment/payment_manage.html'
    form_class = BankCardForm
    success_url = reverse_lazy('dashboard:dashboard_payment:bankcards-list')

    def get_context_data(self, **kwargs):
        ctx = super(BankCardManageView, self).get_context_data(**kwargs)
        ctx['title'] = _("Bank Cards")
        return ctx

    def form_valid(self, form):
        messages.success(self.request, _("Bank card '%s' was updated successfully.") % self.object.name)
        self.object.save()
        return super().form_valid(form)
