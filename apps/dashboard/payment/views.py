  
from django.contrib import messages
from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from oscar.apps.customer.utils import normalise_email
from oscar.core.compat import get_user_model
from oscar.core.loading import get_classes, get_model
from oscar.views import sort_queryset

User = get_user_model()
Bankcard = get_model('payment', 'Bankcard')
(
    BankCardForm
) = get_classes(
    'dashboard.payment.forms',
    ['BankCardForm'])


class BankCardCreateView(generic.CreateView):
    model = Bankcard
    template_name = 'oscar/dashboad/payment/payment_form.html'
    form_class = BankCardForm
    # success_url = reverse_lazy('dashboard:bankcards-list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = _('Add a new bank card')
        return ctx

    def get_success_url(self):
        messages.success(self.request, _("Bank card '%s' was added successfully.") % self.object.name)
        # return reverse('dashboard:bankcards-list')
