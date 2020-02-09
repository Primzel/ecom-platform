from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _, ungettext_lazy
from django_tables2 import LinkColumn, TemplateColumn, A
from oscar.core.loading import get_class, get_model

DashboardTable = get_class('dashboard.tables', 'DashboardTable')
PartnerConfigurableMenu = get_model('configurable_menu', 'PartnerConfigurableMenu')
PartnerConfigurableMenuItem = get_model('configurable_menu', 'PartnerConfigurableMenuItem')


class MenuTable(DashboardTable):
    actions = TemplateColumn(
        template_name='oscar/dashboad/configurable_menu/menuitem_row_actions.html',
        orderable=False)
    class Meta(DashboardTable.Meta):
        model = PartnerConfigurableMenu


class MenuItemTable(DashboardTable):
    name = LinkColumn('dashboard:configurable_menu:partner-configurable-menu-item-update', args=[A('patner_menu_id'),A('pk')])
    description = TemplateColumn(
        template_code='{{ record.description|default:""|striptags'
                      '|cut:"&nbsp;"|truncatewords:6 }}')
    # mark_safe is needed because of
    # https://github.com/bradleyayers/django-tables2/issues/187
    num_children = LinkColumn(
        'dashboard:configurable_menu:partner-configurable-menu-item-details', args=[A('patner_menu_id'),A('pk')],
        verbose_name=mark_safe(_('Number of child categories')),
        accessor='get_num_children',
        orderable=False)
    actions = TemplateColumn(
        template_name='oscar/dashboard/catalogue/category_row_actions.html',
        orderable=False)

    icon = "sitemap"
    caption = ungettext_lazy("%s Category", "%s Categories")

    class Meta(DashboardTable.Meta):
        model = PartnerConfigurableMenuItem
        fields = ('name', 'description')