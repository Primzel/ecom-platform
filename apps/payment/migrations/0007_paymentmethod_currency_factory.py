# Generated by Django 2.2.5 on 2020-06-01 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_paymentmethod_price_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmethod',
            name='currency_factory',
            field=models.IntegerField(default=1, help_text='1 Dollar = 100 cents (1 dollar x Currency Factor(100) = 100)', verbose_name='Currency Factor'),
        ),
    ]
