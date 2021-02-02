from django.db import models, connection
from django.utils.translation import gettext_lazy as _


def get_tenant_specific_upload_folder(instance, filename):
    upload_folder = 'logo/{0}/{1}'.format(
        connection.tenant.name,
        filename
    )
    return upload_folder


class EffectiveSettingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).order_by('-id')

    def get(self):
        return self.get_queryset().first()


# Create your models here.
class Setting(models.Model):
    store_name = models.CharField(max_length=255, verbose_name=_('Store Name'),
                                  help_text=_('Please add store name not more then 255 characters.'))
    tagline = models.CharField(max_length=255, verbose_name=_('Tagline'),
                               help_text=_('Please add store tagline not more then 255 characters.'), default=None,
                               blank=True, null=True)
    logo = models.ImageField(upload_to=get_tenant_specific_upload_folder, verbose_name=_('Store Logo'))
    logo_size = models.CharField(max_length=255, verbose_name=_('Logo Dimension (height x width)'), default='100x100',
                                 help_text=_('Please enter image dimensions not more then 255 characters.'))
    store_from_email = models.EmailField(
        verbose_name=_('From e-mail address.'), null=True, blank=True,
        help_text=_('Please enter email address from you want to send email messages to your customers.')
    )
    is_active = models.BooleanField(default=False)

    effective_settings = EffectiveSettingManager()

    def __str__(self):
        return self.store_name
