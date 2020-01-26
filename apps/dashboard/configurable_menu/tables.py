from django.utils.translation import gettext_lazy as _
from oscar.core.loading import get_class, get_model

DashboardTable = get_class('dashboard.tables', 'DashboardTable')
PartnerConfigurableMenu = get_model('configurable_menu', 'PartnerConfigurableMenu')


class MenuTable(DashboardTable):
    class Meta(DashboardTable.Meta):
        model = PartnerConfigurableMenu