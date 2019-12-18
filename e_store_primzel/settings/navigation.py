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
            }
        ]
    },
]