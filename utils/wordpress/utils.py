import itertools
import logging
from json import load, dump

logger = logging.getLogger('primzel.logger')


def get_categories(client):
    page, end, categories = 1, False, []
    while (not end):
        _categories = client.get_categories(params={'per_page': 100, 'page': page}).json()
        end = True if not _categories else False
        categories += _categories
        logger.debug(
            "page number is {page} value of end is {end} and downloaded={downloaded}".format(page=page, end=end,
                                                                                             downloaded=len(
                                                                                                 _categories)))
        page += 1
    return categories


def get_products(client):
    page, end, products = 1, False, []
    while (not end):
        _products = client.get_products(params={'per_page': 100, 'page': page}).json()
        end = True if not _products else False
        products += _products
        logger.debug("page number is {page} value of end is {end} and downloaded={downloaded}".format(page=page, end=end,downloaded=len(_products)))
        page += 1
    return products


def read_json_file(path):
    with open(path, 'r') as json_file:
        return load(json_file)


def write_json_file(path, json_data):
    dump(json_data, open(path, 'w+'), indent=4)


def format_breadcrumbs(root, categories):
    child_categories = [cat for cat in categories if cat['parent'] == root['id']]
    root['children'] = child_categories
    for child in child_categories:
        format_breadcrumbs(child, categories)


def format_oscar_friendly_breadcrumb_chain(categories):
    root_categories = [cat for cat in categories if cat['parent'] == 0]
    for root in root_categories:
        format_breadcrumbs(root, categories)
    return root_categories


def stringify_breadcrumbs(categories):
    breadcrumbs = []
    for category in categories:
        _breadcrumbs_nested_list = [
            "{category_name}>{_breadcrumb}".format(category_name=category['name'], _breadcrumb=_breadcrumb) for
            _breadcrumb in stringify_breadcrumbs(category['children'])]
        if not _breadcrumbs_nested_list:
            _breadcrumbs_nested_list = [category['name']]
        breadcrumbs += _breadcrumbs_nested_list
    return breadcrumbs


def oscar_friendly_products(woo_products, categories):
    chained_categories = format_oscar_friendly_breadcrumb_chain(categories)
    breadcrumbs_list = stringify_breadcrumbs(chained_categories)
    oscar_friendly_product_list = []
    for woo_product in woo_products:
        oscar_product_dict = {
            "upc": woo_product['sku'],
            "title": woo_product['name'],
            "type": woo_product['type'],
            "status": woo_product['status'],
            "permalink": woo_product['permalink'],
            # "price": woo_product['price'],
            "regular_price": woo_product['regular_price'],
            "sale_price": woo_product['sale_price'],
            "description": woo_product['description'],
            "short_description": woo_product['short_description'],
            "shipping_taxable": woo_product['shipping_taxable'],
            "images": woo_product['images'],
            "attributes": woo_product['attributes'],
            "requires_shipping": woo_product['shipping_required'],
            "track_stock": woo_product['manage_stock'],
            "featured": woo_product['featured'],
            "stock_quantity": woo_product.get('stock_quantity', 0),  # Added stock quantity
            "categories": breadcrumbs_list
        }

        def find_category_ranking(breadcrumbs_list, woo_product):
            for breadcrumbs, category in itertools.product(breadcrumbs_list, woo_product['categories']):
                yield breadcrumbs.find(category["name"]), category["name"]

        product_class = max(find_category_ranking(breadcrumbs_list, woo_product), key=lambda item: item[0])
        product_class = None if product_class[0] == -1 else product_class[1]
        oscar_product_dict['product_class'] = product_class

        product_categories = [category for category in categories for product_cat in woo_product['categories'] if
                              category['id'] == product_cat['id']]

        chained_categories = format_oscar_friendly_breadcrumb_chain(product_categories)
        product_breadcrumbs_list = stringify_breadcrumbs(chained_categories)

        oscar_product_dict['categories'] = product_breadcrumbs_list

        oscar_friendly_product_list.append(oscar_product_dict)

    return oscar_friendly_product_list
