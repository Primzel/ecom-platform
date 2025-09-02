import oscar.apps.catalogue.apps as apps
from django.urls import path
from oscar.core.loading import get_class


class CatalogueConfig(apps.CatalogueConfig):
    name = 'apps.catalogue'

    def ready(self):
        super(CatalogueConfig, self).ready()
        self.quick_detail_view = get_class('catalogue.views', 'ProductDetailView')

    def get_urls(self):
        urls = [
            path('(?P<product_slug>[\w-]*)_(?P<pk>\d+)/quick',
                self.quick_detail_view.as_view(template_name='oscar/catalogue/partials/product_quick_view.html',
                                               enforce_paths=False), name='quick_detail')
        ]
        urls += super(CatalogueConfig, self).get_urls()
        return self.post_process_urls(urls)
