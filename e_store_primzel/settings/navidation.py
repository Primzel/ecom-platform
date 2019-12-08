from oscar.defaults import *

from django.utils.translation import ugettext_lazy as _
OSCAR_DASHBOARD_NAVIGATION += [
    {
        'label': _('Partner Menu'),
        'icon': 'glyphicon-tree-conifer',
        'url_name': 'dashboard:index',
        'children': [
            {
                'label': _('Products'),
                'url_name': 'dashboard:catalogue-product-list',
            }
        ]
    },
]