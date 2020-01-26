# Create your views here.
from django.views import generic
from django_tables2 import SingleTableView
from oscar.core.loading import get_model, get_class
from django.utils.translation import gettext_lazy as _

PartnerConfigurableMenu = get_model('configurable_menu', 'PartnerConfigurableMenu')
PartnerConfigurableMenuForm = get_class('dashboard.configurable_menu.forms', 'PartnerConfigurableMenuForm')
MenuTable = get_class('dashboard.configurable_menu.tables', 'MenuTable')


class PartnerConfigurableMenuCreateView(generic.CreateView):
    template_name = 'oscar/dashboad/configurable_menu/partner_configurable_menu_form.html'
    model = PartnerConfigurableMenu
    form_class = PartnerConfigurableMenuForm

    def get_form_kwargs(self):
        kwargs = super(PartnerConfigurableMenuCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super(PartnerConfigurableMenuCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _("Add a new partner menu")
        return ctx


class ConfigurableMenuListView(SingleTableView):
    table_class = MenuTable
    context_object_name = 'table'
    template_name = 'oscar/dashboad/configurable_menu/partner_configurable_menu_listing.html'
    queryset = PartnerConfigurableMenu.objects.all()

    def get_queryset(self, **kwargs):
        qs = super(ConfigurableMenuListView, self).get_queryset()
        filters = dict()
        if not self.request.user.is_superuser:
            filters.update(dict(partner__in=self.request.user.partners.all()))
        return qs.filter(**filters)

    def get_context_data(self, **kwargs):
        ctx = super(ConfigurableMenuListView, self).get_context_data(**kwargs)
        ctx['title'] = _("Menus")
        return ctx