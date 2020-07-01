from oscar.apps.catalogue.search_handlers import SimpleProductSearchHandler as DefaultSimpleProductSearchHandler

from oscar.core.loading import get_model

Product = get_model('catalogue', 'Product')


class SimpleProductSearchHandler(DefaultSimpleProductSearchHandler):

    def __init__(self, request_data, full_path, categories=None):
        self.categories = categories
        self.kwargs = {'page': request_data.get('page', 1), 'partner': request_data.get('partner', None)}
        self.object_list = self.get_queryset()

    def get_queryset(self):
        qs = Product.objects.browsable().base_queryset()
        partner = self.kwargs.get('partner')
        if partner:
            qs = qs.filter(stockrecords__partner__name=partner)
        if self.categories:
            qs = qs.filter(categories__in=self.categories).distinct()
        return qs
