from django.utils.translation import gettext_lazy as _
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
                'url_name': 'dashboard:dashboard_payment:bankcards-list',
            },
            {
                'label': _('Payment methods'),
                'url_name': 'dashboard:dashboard_payment:payment_methods-list',
            },
            {
                'label': _('Source Types'),
                'url_name': 'dashboard:dashboard_payment:source_types-list',
            },
            {
                'label': _('Sources'),
                'url_name': 'dashboard:dashboard_payment:sources-list',
            },
            {
                'label': _('Transactions'),
                'url_name': 'dashboard:dashboard_payment:transactions-list',
            },
            {
                'label': _('Available payment gateways'),
                'url_name': 'dashboard:dashboard_payment:payment_gateways-list',
            },
        ]
    },
    {
        'label': _('Settings'),
        'icon': 'glyphicon-tree-conifer',
        'children': [
            {
                'label': _('Banners'),
                'url_name': 'dashboard:dashboard_banners:banners-listing',
            },
            {
                'label': _('New Banner'),
                'url_name': 'dashboard:dashboard_banners:banners-create',
            }
        ]
    }
]
