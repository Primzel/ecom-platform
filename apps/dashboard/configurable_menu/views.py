# Create your views here.
from django.views import generic
from oscar.core.loading import get_model, get_class
from django.utils.translation import gettext_lazy as _
PartnerConfigurableMenu = get_model('configurable_menu', 'PartnerConfigurableMenu')
PartnerConfigurableMenuForm = get_class('dashboard.configurable_menu.forms', 'PartnerConfigurableMenuForm')


class PartnerConfigurableMenuCreateView(generic.CreateView):
    template_name = 'oscar/dashboard/catalogue/category_form.html'
    model = PartnerConfigurableMenu
    form_class = PartnerConfigurableMenuForm

    def get_context_data(self, **kwargs):
        ctx = dict()
        ctx['title'] = _("Add a new partner menu")
        return ctx
