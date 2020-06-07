  
from django.contrib import messages
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
        return super().get_success_url()
        # return reverse('dashboard:bankcards-list')
