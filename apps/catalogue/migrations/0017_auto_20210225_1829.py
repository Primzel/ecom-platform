# Generated by Django 2.2.5 on 2021-02-25 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0016_auto_20190327_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='depth',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
