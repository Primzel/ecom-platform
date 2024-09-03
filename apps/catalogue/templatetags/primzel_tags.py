from django import template
from oscar.apps.catalogue.models import ProductAttributeValue
from oscar.apps.offer.models import ConditionalOffer, Benefit, Condition, Range
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
        for attribute_value in ProductAttributeValue.objects.filter(product=child).select_related('product',
                                                                                                  'attribute'):
            attribute_name, value = attribute_value.attribute.name, attribute_value.value

            descriptors.setdefault(attribute_name, {}).setdefault(value, set()).add(attribute_value.product_id)

    # In general, we want things sorted when we output them
    return sorted((attribute, value_map.items()) for attribute, value_map in descriptors.items())


@register.inclusion_tag('oscar/catalogue/partials/variant_descriptors.html')
def render_variant_descriptors(product):
    return {
        'product': product,
        'descriptors': _get_variant_descriptors(product)
    }

@register.simple_tag
def get_discounted_price(product):
    debug_logs = []  # List to accumulate debug messages

    try:
        # Correctly assign product_id from the product object
        product_id = product.id
        debug_logs.append(f"Product ID: {product_id}")

        # Check if the product is discountable
        if not product.is_discountable:
            debug_logs.append("Product is not discountable")
            return {'logs': debug_logs, 'discounted_price': None}

        # Get the category ID of the first category associated with the product
        category = product.productcategory_set.first()
        if category:
            category_id = category.category_id
            debug_logs.append(f"Category ID: {category_id}")
        else:
            debug_logs.append("No category found for product")
            return {'logs': debug_logs, 'discounted_price': None}

        # Fetch all open site-wide offers
        offers = ConditionalOffer.objects.filter(
            offer_type='Site',
            status='Open'
        )
        debug_logs.append(f"Offers found: {offers.count()}")

        if not offers.exists():
            debug_logs.append("No open site-wide offers")
            return {'logs': debug_logs, 'discounted_price': None}

        # Iterate over the offers and apply the logic
        for offer in offers:
            debug_logs.append(f"Processing offer ID: {offer.id}")

            # Get the associated Benefit and Condition objects
            benefit = Benefit.objects.filter(id=offer.benefit_id).first()
            condition = Condition.objects.filter(id=offer.condition_id).first()

            # Continue to the next offer if either Benefit or Condition is missing
            if not benefit or not condition:
                debug_logs.append(f"Skipping offer ID {offer.id} due to missing Benefit or Condition")
                continue

            # Only proceed if the benefit type is 'Percentage' or 'Fixed'
            if benefit.type not in ['Percentage', 'Fixed']:
                debug_logs.append(f"Skipping offer ID {offer.id} due to invalid benefit type: {benefit.type}")
                continue

            # Ensure the condition type is 'Value'
            if condition.type != 'Value':
                debug_logs.append(f"Skipping offer ID {offer.id} due to invalid condition type: {condition.type}")
                continue

            # Check that the range IDs match between benefit and condition
            if benefit.range_id != condition.range_id:
                debug_logs.append(f"Skipping offer ID {offer.id} due to mismatched range IDs")
                continue

            # Fetch the associated Range object
            offer_range = Range.objects.filter(id=benefit.range_id, is_public=True).first()

            if not offer_range:
                debug_logs.append(f"Skipping offer ID {offer.id} due to missing Range or Range is not public")
                continue

            # Check if the range includes all products or the specific product's category
            if not offer_range.includes_all_products:
                # Check if the product category is included in the range
                if not offer_range.classes.filter(id=category_id).exists():
                    debug_logs.append(f"Skipping offer ID {offer.id} as category ID {category_id} is not included in the range")
                    continue

            # Fetch the stock record to get the price
            stock_record = StockRecord.objects.filter(product_id=product_id).first()
            if not stock_record:
                debug_logs.append(f"Skipping offer ID {offer.id} as no stock record found for product ID {product_id}")
                continue

            price = stock_record.price
            debug_logs.append(f"Price from stock record: {price}")

            # Check if the price meets the condition value
            if price < condition.value:
                debug_logs.append(f"Skipping offer ID {offer.id} as price {price} does not exceed condition value {condition.value}")
                continue

            # Calculate the sale price based on the benefit type
            if benefit.type == 'Percentage':
                sale_price = price - (price * benefit.value / 100)
                debug_logs.append(f"Calculated sale price (Percentage): {sale_price}")
            elif benefit.type == 'Fixed':
                sale_price = price - benefit.value
                debug_logs.append(f"Calculated sale price (Fixed): {sale_price}")

            # Return the calculated sale price and debug logs
            return {'logs': debug_logs, 'discounted_price': sale_price}

        # Return debug logs if no applicable offer is found
        debug_logs.append("No applicable offer found")
        return {'logs': debug_logs, 'discounted_price': None}

    except Exception as e:
        debug_logs.append(f"An error occurred: {e}")
        return {'logs': debug_logs, 'discounted_price': None}
