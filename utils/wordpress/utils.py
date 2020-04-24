import logging
from json import load, dump

logger = logging.getLogger('primzel.logger')


def get_categories(client):
    page, end, categories = 1, False, []
    while (not end):
        _categories = client.get_categories(params={'per_page': 100, 'page': page}).json()
        end = True if not _categories else False
        categories += _categories
        logger.debug("page number is {page} value of end is {end} and downloaded={downloaded}".format(page=page, end=end,
                                                                                                     downloaded=len(
                                                                                                         _categories)))
        page += 1
    return categories


def get_products(hoko_client):
    page, end, products = 1, False, []
    while (not end):
        _products = hoko_client.get_products(params={'per_page': 100, 'page': page}).json()
        end = True if not _products else False
        products += _products
        logger.debug("page number is {page} value of end is {end} and downloaded={downloaded}".format(page=page, end=end,
                                                                                                     downloaded=len(
                                                                                                         _products)))
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
