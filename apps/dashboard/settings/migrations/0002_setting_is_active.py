# Generated by Django 2.2.5 on 2020-05-29 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]