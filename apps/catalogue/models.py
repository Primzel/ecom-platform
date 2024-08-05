from django.db import models
from oscar.apps.catalogue.abstract_models import AbstractProduct
from oscar.core.loading import is_model_registered

if not is_model_registered('catalogue', 'Product'):
    class Product(AbstractProduct):
        regular_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
        sale_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    from oscar.apps.catalogue.models import *  # Import other default Oscar models