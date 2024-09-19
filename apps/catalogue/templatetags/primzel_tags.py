from django import template
from oscar.apps.catalogue.models import ProductAttributeValue
from oscar.apps.partner.models import StockRecord 

register = template.Library()


@register.simple_tag(takes_context=True)
def product_options(context, product):
    options = dict([(op.name.lower(), set()) for op in product.options.all()])
    for child_product in product.children.all():
        for child_product_option in child_product.attribute_values.all():
            option_group_name = child_product_option.value_option.group.name.lower()
            if option_group_name in options:
                options[option_group_name.lower()].add(child_product_option.value_option.option)
    return options


# templatetags.py

def _get_variant_descriptors(product):
    descriptors = {}
    for child in product.children.all():
        stock_record = StockRecord.objects.filter(product_id=child.id).first()
        if stock_record:
            num_in_stock = stock_record.num_in_stock or 0
        else:
            num_in_stock = 0  # Handle the case where no stock record exists

        if num_in_stock > 0:
            for attribute_value in ProductAttributeValue.objects.filter(product=child).select_related('product', 'attribute'):
                attribute_name, value = attribute_value.attribute.name, attribute_value.value

                # Add product IDs for attribute values
                descriptors.setdefault(attribute_name, {}).setdefault(value, set()).add(attribute_value.product_id)

    # In general, we want things sorted when we output them
    return sorted((attribute, sorted(value_map.items())) for attribute, value_map in descriptors.items())


@register.inclusion_tag('oscar/catalogue/partials/variant_descriptors.html')
def render_variant_descriptors(product):
    return {
        'product': product,
        'descriptors': _get_variant_descriptors(product)
    }
