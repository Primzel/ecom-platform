# Generated by Django 2.2.5 on 2021-02-02 13:44

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0002_bannerimage_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannerimage',
            name='color',
            field=colorfield.fields.ColorField(default='#FFFFFF', max_length=18),
        ),
    ]
