# Generated by Django 2.2.5 on 2020-05-29 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0002_setting_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='tagline',
            field=models.CharField(blank=True, default=None, help_text='Please add store tagline not more then 255 characters.', max_length=255, null=True, verbose_name='Tagline'),
        ),
    ]
