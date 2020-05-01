import logging
import os
import urllib

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from oscar.apps.catalogue.categories import create_from_breadcrumbs
from oscar.apps.catalogue.models import Product, ProductClass, slugify, AttributeOptionGroup, AttributeOption, \
    ProductAttribute, ProductImage, ProductCategory

from utils.wordpress.client import Client
from utils.wordpress.utils import stringify_breadcrumbs, format_oscar_friendly_breadcrumb_chain, get_categories, \
    oscar_friendly_products, get_products

logger = logging.getLogger('primzel.logger')


def import_categories_from_wordpress(*args, **kwargs):
    """
    The function is used to import categories from woocommerce host to current tenant.
    :param host: base url of woocommerce host.
    :param consumer_key: woocommerce consumer key
    :param consumer_secret: woocommerce consumer secret
    :return:
    """
    print(kwargs)
    host = kwargs.get('host', "http://www.hoko.pk")
    consumer_key = kwargs.get('consumer_key', "ck_5370bb23c2327f912da64abf4ced3e0c5c8363d2")
    consumer_secret = kwargs.get('consumer_secret', "cs_cbdd51bafd47fa9356401f09fa321e0f95080f7e")

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
    woo_products = get_products(client=client)
    products = oscar_friendly_products(woo_products, categories)

    for product in products:
        upc = product['upc']
        if upc:
            product_class, t_created = ProductClass.objects.get_or_create(name=product['type'],
                                                                          slug=slugify(product['type']))
            oscar_product, p_created = Product.objects.get_or_create(upc=upc, product_class=product_class)

            if t_created:
                product_class.requires_shipping = product['requires_shipping']
                product_class.track_stock = product['track_stock']
                product_class.save(update_fields=['requires_shipping', 'track_stock'])

            if p_created:
                oscar_product.title = product['title']
                oscar_product.description = product['description']
                for woo_option_group in product['attributes']:
                    option_group, opg_created = AttributeOptionGroup.objects.get_or_create(
                        name=woo_option_group['name'])
                    for woo_option in woo_option_group['options']:
                        AttributeOption.objects.get_or_create(group=option_group, option=woo_option)

                    ProductAttribute.objects.get_or_create(
                        product_class=product_class, name=option_group.name, code=slugify(option_group.name),
                        type='option', option_group=option_group)
                oscar_product.product_class = product_class
                oscar_product.save()

                for woo_image in product['images']:
                    product_image = ProductImage()
                    img_temp = NamedTemporaryFile(delete=True)

                    img_temp.write(urllib.request.urlopen(woo_image['src']).read())
                    img_temp.flush()
                    product_image.caption = woo_image['alt']
                    product_image.product = oscar_product
                    product_image.original.save(os.path.basename(woo_image['src']), File(img_temp))

                    product_image.save()
            for breadcrumbs in product['categories']:
                category_string = create_from_breadcrumbs(breadcrumbs)
                ProductCategory.objects.update_or_create(product=oscar_product, category=category_string)

        else:
            logger.info('missing sku value for product {permalink}'.format(permalink=product['permalink']))
            continue
