# Generated by Django 2.2.5 on 2021-02-25 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configurable_menu', '0005_auto_20200529_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partnerconfigurablemenuitem',
            name='depth',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
