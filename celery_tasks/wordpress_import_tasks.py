import logging
import os
import urllib
import time

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import IntegrityError
from oscar.apps.catalogue.categories import create_from_breadcrumbs
from apps.catalogue.models import Product, ProductClass, AttributeOptionGroup, AttributeOption, \
    ProductAttribute, ProductImage, ProductCategory
from apps.partner.models import StockRecord, Partner
from django.utils.text import slugify

from utils.wordpress.client import Client
from utils.wordpress.utils import stringify_breadcrumbs, format_oscar_friendly_breadcrumb_chain, get_categories, \
    oscar_friendly_products, get_products

logger = logging.getLogger('primzel.logger')


def import_categories_from_wordpress(*args, **kwargs):
    """
    The function is used to import categories and products from WooCommerce host to the current tenant.
    :param host: base url of WooCommerce host.
    :param consumer_key: WooCommerce consumer key
    :param consumer_secret: WooCommerce consumer secret
    :return:
    """

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

    logger.info('Starting category import...')
    def create_category(breadcrumbs_list):
        for breadcrumb in breadcrumbs_list:
            create_from_breadcrumbs(breadcrumb)

    create_category(breadcrumbs_list)
    logger.info('Category import completed from {wordpress_host}'.format(wordpress_host=host))

    logger.info('================== PRODUCT IMPORT STARTED ===============')
    woo_products = get_products(client=client)
    
    logger.info('================== PRODUCT IMPORT COMPLETED ===============')
    time.sleep(5)
    products = oscar_friendly_products(woo_products, categories)
    logger.info('================== OSCAR FRIENDLYPRODUCT COMPLETED ===============')
    time.sleep(5)

    partner, created = Partner.objects.get_or_create(name='Default Partner')
    
    for product in products:
        upc = product['upc']
        if upc:
            logger.info(f"Importing product: UPC={upc}, Title={product['title']}")
            try:
                product_class, t_created = ProductClass.objects.get_or_create(
                    name=product['product_class'],
                    slug=slugify(product['product_class'])
                )
                oscar_product, p_created = Product.objects.get_or_create(
                    upc=upc,
                    defaults={
                        'product_class': product_class,
                        'title': product['title'],
                        'description': product['description'],
                        'regular_price': product.get('regular_price'),  # Regular price
                        'sale_price': product.get('sale_price')  # Sale price
                    }
                )

                if t_created:
                    product_class.requires_shipping = product['requires_shipping']
                    product_class.track_stock = product['track_stock']
                    product_class.save(update_fields=['requires_shipping', 'track_stock'])

                for woo_option_group in product['attributes']:
                    option_group, opg_created = AttributeOptionGroup.objects.get_or_create(
                        name=woo_option_group['name']
                    )
                    for woo_option in woo_option_group['options']:
                        AttributeOption.objects.get_or_create(group=option_group, option=woo_option)

                    try:
                        ProductAttribute.objects.get_or_create(
                            product_class=product_class,
                            name=option_group.name,
                            code=slugify(option_group.name),
                            type='option',
                            option_group=option_group
                        )
                    except IntegrityError as e:
                        logger.error(f"IntegrityError for attribute {option_group.name}: {e}")

                if p_created:
                    oscar_product.product_class = product_class
                    oscar_product.save()

                    print('======================image storing started======================')
                    time.sleep(5)
                    # Inside your import function
                    for woo_image in product['images']:
                        try:
                            img_temp = NamedTemporaryFile(delete=True)
                            logger.info(f"Downloading image from {woo_image['src']}")
                            img_temp.write(urllib.request.urlopen(woo_image['src']).read())
                            img_temp.flush()
                            
                            product_image = ProductImage(
                                caption=woo_image['alt'],
                                product=oscar_product
                            )
                            product_image.original.save(os.path.basename(woo_image['src']), File(img_temp))
                            product_image.save()

                            logger.info(f"======================Image saved for product {oscar_product.upc}: {woo_image['src']}===================")
                        except Exception as e:
                            logger.error(f"===================Failed to save image for product {oscar_product.upc}: {e}====================")
                    print('======================image storing completed======================')
                    time.sleep(5)

                for breadcrumbs in product['categories']:
                    category_string = create_from_breadcrumbs(breadcrumbs)
                    ProductCategory.objects.update_or_create(product=oscar_product, category=category_string)

                # Handle stock quantity
                stock_quantity = product.get('stock_quantity', 0)
                if stock_quantity is None:
                    stock_quantity = 0
                if stock_quantity >= 0:  # Ensure non-negative stock quantity
                    # Create or update stock record
                    StockRecord.objects.update_or_create(
                        product=oscar_product,
                        partner=Partner.objects.first(),  # Adjust as needed
                        partner_sku=upc,
                        defaults={
                            'num_in_stock': stock_quantity,
                            'price_currency': 'PKR',  # Adjust currency if needed
                            'price': product.get('regular_price'),
                            'low_stock_threshold': 5  # Example threshold, adjust as needed
                        }
                    )

                logger.info(f"Product imported: UPC={upc}, Title={product['title']}")
            except Exception as e:
                logger.error(f"Failed to import product {upc}: {e}")
                continue
        else:
            logger.info('Missing SKU value for product {permalink}'.format(permalink=product['permalink']))
            continue
logger.info('Product import completed.')