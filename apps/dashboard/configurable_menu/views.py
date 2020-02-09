# Create your views here.
from django.contrib import messages
from django.http import Http404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django_tables2 import SingleTableView, SingleTableMixin
from oscar.core.loading import get_model, get_class

from apps.dashboard.configurable_menu.forms import PartnerMenuItemForm
from apps.dashboard.configurable_menu.tables import MenuItemTable

PartnerConfigurableMenu = get_model('configurable_menu', 'PartnerConfigurableMenu')
PartnerConfigurableMenuForm = get_class('dashboard.configurable_menu.forms', 'PartnerConfigurableMenuForm')
MenuTable = get_class('dashboard.configurable_menu.tables', 'MenuTable')
PartnerConfigurableMenuItem = get_model('configurable_menu', 'PartnerConfigurableMenuItem')


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


class MenuItemListView(SingleTableView):
    template_name = 'oscar/dashboad/configurable_menu/menuitems_listing.html'
    table_class = MenuItemTable
    context_table_name = 'menuitems'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data(*args,**kwargs)
        return self.render_to_response(context)

    def get_queryset(self):
        return PartnerConfigurableMenuItem.get_root_nodes()

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['child_categories'] = PartnerConfigurableMenuItem.get_root_nodes()
        ctx['menu_id'] = kwargs.get('menu_id')
        return ctx


class MenuItemListMixin(object):

    def get_success_url(self):
        parent = self.object.get_parent()
        menu_id = self.kwargs.get('menu_id')
        if parent is None:
            return reverse("dashboard:configurable_menu:partner-configurable-menu-items", args=(menu_id,))
        else:
            return reverse("dashboard:configurable_menu:partner-configurable-menu-item-details",
                           args=(menu_id,parent.pk,))


class MenuItemCreateView(MenuItemListMixin, generic.CreateView):
    template_name = 'oscar/dashboard/catalogue/category_form.html'
    model = PartnerConfigurableMenuItem
    form_class = PartnerMenuItemForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = _("Add a new category")
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Category created successfully"))
        return super().get_success_url()

    def get_initial(self):
        # set child category if set in the URL kwargs
        initial = super().get_initial()
        initial['patner_menu'] = self.kwargs.get('menu_id', None)
        if 'parent' in self.kwargs:
            initial['_ref_node_id'] = self.kwargs['parent']
        return initial


class MenuItemDetailListView(SingleTableMixin, generic.DetailView):
    template_name = 'oscar/dashboad/configurable_menu/menuitems_listing.html'
    model = PartnerConfigurableMenuItem
    context_object_name = 'menuitem'
    table_class = MenuItemTable
    context_table_name = 'menuitems'

    def get_table_data(self):
        return self.object.get_children()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data(object=self.object,*args,**kwargs))

    def get_context_data(self, *args, **kwargs):
        ctx = super(MenuItemDetailListView,self).get_context_data(*args, **kwargs)
        ctx['child_categories'] = self.object.get_children()
        ctx['ancestors'] = self.object.get_ancestors_and_self()
        ctx['menu_id'] = kwargs.get('menu_id')
        return ctx


class CategoryUpdateView(MenuItemListMixin, generic.UpdateView):
    template_name = 'oscar/dashboard/catalogue/category_form.html'
    model = PartnerConfigurableMenuItem
    form_class = PartnerMenuItemForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = _("Update menuitem '%s'") % self.object.name
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Category updated successfully"))
        return super().get_success_url()
