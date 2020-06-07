from django.utils.translation import ugettext_lazy as _
from oscar.defaults import *

OSCAR_DASHBOARD_NAVIGATION += [
    {
        'label': _('Configurable Partner Menu'),
        'icon': 'glyphicon-tree-conifer',
        'children': [
            {
                'label': _('Create Menu'),
                'url_name': 'dashboard:configurable_menu:partner-configurable-menu-create',
            },
            {
                'label': _('All Menus'),
                'url_name': 'dashboard:configurable_menu:partner-configurable-menu-listing',
            }
        ]
    },
    {
        'label': _('Payment'),
        'icon': 'glyphicon-usd',
        'children': [
            {
                'label': _('Bankcards'),
                'url_name': 'dashboard:dashboard_payment:bankcard-create',
            },
            {
                'label': _('Payment methods'),
                'url_name': 'dashboard:configurable_menu:partner-configurable-menu-listing',
            },
            {
                'label': _('Source Types'),
                'url_name': 'dashboard:configurable_menu:partner-configurable-menu-listing',
            },
            {
                'label': _('Sources'),
                'url_name': 'dashboard:configurable_menu:partner-configurable-menu-listing',
            },
            {
                'label': _('Transactions'),
                'url_name': 'dashboard:configurable_menu:partner-configurable-menu-listing',
            },
            {
                'label': _('Available payment gateways'),
                'url_name': 'dashboard:configurable_menu:partner-configurable-menu-listing',
            },
        ]
    },
    {
        'label': _('Settings'),
        'icon': 'glyphicon-tree-conifer',
        'url_name': 'dashboard:reports-index',
    },
]
