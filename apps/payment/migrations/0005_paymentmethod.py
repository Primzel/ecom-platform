# Generated by Django 2.2.5 on 2020-05-31 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment_gateways', '0001_initial'),
        ('payment', '0004_auto_20181115_1953'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('publishable_key', models.CharField(help_text='Publishable key', max_length=1024)),
                ('secret_key', models.CharField(help_text='Secret key', max_length=1024)),
                ('is_active', models.BooleanField(default=False)),
                ('payment_gateway', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='integrations', to='payment_gateways.AvailablePaymentGateway')),
            ],
        ),
    ]
