# from django.conf.urls import include, url  # < Django-2.0
from django.urls import include, path  # > Django-2.0
from django.utils.translation import gettext_lazy as _
from oscar.core.application import OscarDashboardConfig
from oscar.core.loading import get_class


class ConfigurableMenuConfig(OscarDashboardConfig):
    name = 'apps.dashboard.configurable_menu'
    label = 'configurable_menu'
    verbose_name = _('Configurable Menu')
    namespace = 'configurable_menu'
    default_permissions = ['is_staff']
    permissions_map = _map = {
        'partner-configurable-menu-create': (['is_staff'], ['partner.dashboard_access']),
        'partner-configurable-menu-listing': (['is_staff'], ['partner.dashboard_access']),
        'partner-configurable-menu-items': (['is_staff'], ['partner.dashboard_access']),
        'partner-configurable-menu-item-create': (['is_staff'], ['partner.dashboard_access']),
        'partner-configurable-child-menu-item-create': (['is_staff'], ['partner.dashboard_access']),
        'partner-configurable-menu-item-details': (['is_staff'], ['partner.dashboard_access']),
        'partner-configurable-menu-item-update': (['is_staff'], ['partner.dashboard_access']),
    }

    def ready(self):
        self.partner_configurable_menu_create_view = get_class('dashboard.configurable_menu.views',
                                                               'PartnerConfigurableMenuCreateView')
        self.partner_configurable_menu_listing = get_class('dashboard.configurable_menu.views',
                                                           'ConfigurableMenuListView')
        self.partner_configurable_menu_items = get_class('dashboard.configurable_menu.views', 'MenuItemListView')
        self.partner_configurable_menu_item_create = get_class('dashboard.configurable_menu.views',
                                                               'MenuItemCreateView')
        self.partner_configurable_menu_detail = get_class('dashboard.configurable_menu.views',
                                                               'MenuItemDetailListView')
        self.partner_configurable_menu_item_update = get_class('dashboard.configurable_menu.views',
                                                               'CategoryUpdateView')

    def get_urls(self):
        urls = [
            path(r'create/',
                 self.partner_configurable_menu_create_view.as_view(), name='partner-configurable-menu-create'),
            path(r'',
                 self.partner_configurable_menu_listing.as_view(), name='partner-configurable-menu-listing'),
            path(r'<int:menu_id>/menuitems',
                 self.partner_configurable_menu_items.as_view(), name='partner-configurable-menu-items'),
            path(r'<int:menu_id>/menuitems/create',
                 self.partner_configurable_menu_item_create.as_view(),
                 name='partner-configurable-menu-item-create'),
            path(r'<int:menu_id>/menuitems/create/<int:parent>',
                 self.partner_configurable_menu_item_create.as_view(),
                 name='partner-configurable-child-menu-item-create'),
            path(r'<int:menu_id>/menuitems/<int:pk>/',
                 self.partner_configurable_menu_detail.as_view(),
                 name='partner-configurable-menu-item-details'),
            path(r'<int:menu_id>/menuitems/<int:pk>/update/',
                 self.partner_configurable_menu_item_update.as_view(),
                 name='partner-configurable-menu-item-update'),
        ]
        return self.post_process_urls(urls)
