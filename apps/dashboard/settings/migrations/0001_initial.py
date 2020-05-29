# Generated by Django 2.2.5 on 2020-05-29 19:17

import apps.dashboard.settings.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(help_text='Please add store name not more then 255 characters.', max_length=255, verbose_name='Store Name')),
                ('logo', models.ImageField(upload_to=apps.dashboard.settings.models.get_tenant_specific_upload_folder, verbose_name='Store Logo')),
            ],
        ),
    ]
