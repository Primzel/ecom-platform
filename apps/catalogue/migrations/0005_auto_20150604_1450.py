# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0004_auto_20150217_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_class',
            field=models.ForeignKey(related_name='products', on_delete=django.db.models.deletion.PROTECT, blank=True, to='catalogue.ProductClass', help_text='Choose what type of product this is', null=True, verbose_name='Product type'),
        ),
    ]
