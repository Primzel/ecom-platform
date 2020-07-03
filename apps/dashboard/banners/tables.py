from django.utils.translation import ungettext_lazy
from django_tables2 import TemplateColumn
from oscar.core.loading import get_class, get_model

DashboardTable = get_class('dashboard.tables', 'DashboardTable')
Banner = get_model('banners', 'Banner')


class BannerTable(DashboardTable):
    caption = ungettext_lazy("%d Banner", "%d Banner")
    actions = TemplateColumn(
        template_name='banners/dashboard/partials/actions.html',
        orderable=False)

    class Meta(DashboardTable.Meta):
        model = Banner
