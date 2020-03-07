# Generated by Django 2.2.5 on 2020-02-14 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0016_auto_20190327_0757'),
        ('configurable_menu', '0003_partnerconfigurablemenu_partner'),
    ]

    operations = [
        migrations.AddField(
            model_name='partnerconfigurablemenuitem',
            name='included_categories',
            field=models.ManyToManyField(blank=True, related_name='menu_includes', to='catalogue.Category', verbose_name='Included Categories'),
        ),
    ]