from six import with_metaclass
from django import template
from oscar.core.loading import get_model

register = template.Library()
PartnerConfigurableMenuItem = get_model("configurable_menu", "PartnerConfigurableMenuItem")


class PassThrough(object):
    def __init__(self, name):
        self.name = name

    def __get__(self, obj, objtype):
        if obj is None:
            return self

        return getattr(obj.category, self.name)


class MenuItemFieldPassThroughMetaClass(type):
    """
    Add accessors for category fields to whichever class is of this type.
    """

    def __new__(cls, name, bases, attrs):
        field_accessors = {}
        for field in PartnerConfigurableMenuItem._meta.get_fields():
            name = field.name
            field_accessors[name] = PassThrough(name)

        # attrs win of silly field accessors
        field_accessors.update(attrs)
        return type.__new__(cls, name, bases, field_accessors)


class CheapMenuItemInfo(with_metaclass(MenuItemFieldPassThroughMetaClass, dict)):
    """
    Wrapper class for Category.

    Besides allowing inclusion of extra info, useful while rendering a template,
    this class hides any expensive properties people should not use by accident
    in templates.

    This replaces both the node as the info object returned by the ``category_tree``
    templatetag, so it mimics a tuple of 2 items (which are the same) for
    backwards compatibility.
    """

    def __init__(self, category, **info):
        super().__init__(info)
        self.category = category

    @property
    def pk(self):
        return self.category.pk

    def get_absolute_url(self):
        return self["url"]

    def __len__(self):
        "Mimic a tuple of 2 items"
        return 2

    def __iter__(self):
        "be an iterable of 2 times the same item"
        yield self
        yield self


@register.simple_tag(name="menu_tree")  # noqa: C901 too complex
def get_annotated_list(depth=None, parent=None):
    """
    Gets an annotated list from a tree branch.

    Borrows heavily from treebeard's get_annotated_list
    """
    # 'depth' is the backwards-compatible name for the template tag,
    # 'max_depth' is the better variable name.
    max_depth = depth

    if parent:
        menu_items = parent.get_descendants()
        if max_depth is not None:
            max_depth += parent.get_depth()
    else:
        menu_items = PartnerConfigurableMenuItem.get_tree().prefetch_related('included_categories').filter(
            patner_menu__is_primary=True)

    if max_depth is not None:
        menu_items = menu_items.filter(depth__lte=max_depth)

    menu_row = []
    menu_rows = [menu_row, ]
    for menu_item in menu_items:
        menu_row.append(menu_item)
        if len(menu_row) % 3 == 0:
            menu_row = []
            menu_rows.append(menu_row)

    return menu_rows
