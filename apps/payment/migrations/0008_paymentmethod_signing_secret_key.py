# Generated by Django 2.2.5 on 2020-06-02 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_paymentmethod_currency_factory'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmethod',
            name='signing_secret_key',
            field=models.CharField(blank=True, help_text='Signing secret key', max_length=1024, null=True),
        ),
    ]
