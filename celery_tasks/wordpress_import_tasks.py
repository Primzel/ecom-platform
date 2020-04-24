import logging

from oscar.apps.catalogue.categories import create_from_breadcrumbs

from utils.wordpress.client import Client
from utils.wordpress.utils import stringify_breadcrumbs, format_oscar_friendly_breadcrumb_chain, get_categories

logger = logging.getLogger('primzel.logger')


def import_categories_from_wordpress(host="http://www.hoko.pk",
                                     consumer_key="ck_5370bb23c2327f912da64abf4ced3e0c5c8363d2",
                                     consumer_secret="cs_cbdd51bafd47fa9356401f09fa321e0f95080f7e"):
    """
    The function is used to import categories from woocommerce host to current tenant.
    :param host: base url of woocommerce host.
    :param consumer_key: woocommerce consumer key
    :param consumer_secret: woocommerce consumer secret
    :return:
    """
    kwargs = dict(
        url=host,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret
    )
    client = Client(**kwargs)
    categories = get_categories(client)
    chained_categories = format_oscar_friendly_breadcrumb_chain(categories)
    breadcrumbs_list = stringify_breadcrumbs(chained_categories)

    def create_category(breadcrumbs_list):
        for breadcrumb in breadcrumbs_list:
            create_from_breadcrumbs(breadcrumb)

    create_category(breadcrumbs_list)
    logger.info('category import completed from {wordpress_host}'.format(wordpress_host=host))
