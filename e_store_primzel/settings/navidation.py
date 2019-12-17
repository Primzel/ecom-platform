from django.utils.translation import ugettext_lazy as _
from oscar.defaults import *

OSCAR_DASHBOARD_NAVIGATION += [
    {
        'label': _('Partner Menu'),
        'icon': 'glyphicon-tree-conifer',
        'children': [
            {
                'label': _('asda'),
                'url_name': 'dashboard:partner-configurable-menu-create',
            }
        ]
    },
]