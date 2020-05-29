from django.db import models, connection
from django.utils.translation import gettext_lazy as _


def get_tenant_specific_upload_folder(instance, filename):
    upload_folder = 'logo/{0}/{1}'.format(
        connection.tenant,
        filename
    )
    return upload_folder


# Create your models here.
class Setting(models.Model):
    store_name = models.CharField(max_length=255, verbose_name=_('Store Name'),
                                  help_text=_('Please add store name not more then 255 characters.'))
    tagline = models.CharField(max_length=255, verbose_name=_('Tagline'),
                               help_text=_('Please add store tagline not more then 255 characters.'), default=None,
                               blank=True, null=True)
    logo = models.ImageField(upload_to=get_tenant_specific_upload_folder, verbose_name=_('Store Logo'))
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.store_name
