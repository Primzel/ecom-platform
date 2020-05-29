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
        'label': _('Settings'),
        'icon': 'glyphicon-tree-conifer',
        'url_name': 'dashboard:reports-index',
    }
]
