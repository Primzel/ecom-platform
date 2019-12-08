import oscar.apps.dashboard.catalogue.apps as apps
from oscar.core.loading import get_class


class CatalogueDashboardConfig(apps.CatalogueDashboardConfig):
    name = 'apps.dashboard.catalogue'
    permissions_map = _map = {
        'catalogue-product': (['is_staff'], ['partner.dashboard_access']),
        'catalogue-product-create': (['is_staff'],
                                     ['partner.dashboard_access']),
        'catalogue-product-list': (['is_staff'], ['partner.dashboard_access']),
        'catalogue-product-delete': (['is_staff'],
                                     ['partner.dashboard_access']),
        'catalogue-product-lookup': (['is_staff'],
                                     ['partner.dashboard_access']),
        'catalogue-category-list': (['is_staff'],
                                    ['partner.dashboard_access']),
        'catalogue-category-detail-list': (['is_staff'],
                                           ['partner.dashboard_access']),
        'catalogue-category-create': (['is_staff'],
                                      ['partner.dashboard_access']),
        'catalogue-category-create-child': (['is_staff'],
                                            ['partner.dashboard_access']),
        'catalogue-category-update': (['is_staff'],
                                      ['partner.dashboard_access']),
        'catalogue-category-delete': (['is_staff'],
                                      ['partner.dashboard_access']),
    }

    def ready(self):
        super(CatalogueDashboardConfig, self).ready()
        self.category_list_view = get_class('dashboard.catalogue.views', 'CategoryListView')
