# Generated by Django 2.2.5 on 2020-05-31 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_gateways', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='availablepaymentgateway',
            name='slug',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
    ]
