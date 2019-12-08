from oscar.apps.dashboard.catalogue.views import CategoryListView
from oscar.core.loading import get_classes, get_model

Category = get_model('catalogue', 'Category')


class CategoryListView(CategoryListView):
    def get_queryset(self):
        return Category.get_root_nodes()
