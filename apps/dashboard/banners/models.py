from django.db import models, connection
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from oscar.models.fields import AutoSlugField


def get_tenant_specific_upload_folder(instance, filename):
    upload_folder = 'banners/{0}/{1}'.format(
        connection.tenant.name,
        filename
    )
    return upload_folder


class Banner(models.Model):
    title = models.CharField(verbose_name='Banner Title', max_length=255)
    slug = AutoSlugField(_('Slug'), max_length=128, unique=True, populate_from='title')

    def get_absolute_url(self):
        return reverse('dashboard:dashboard_banners:banners-listing')

    def __str__(self):
        return "{title}".format(title=self.title)


class BannerImage(models.Model):
    banner = models.ForeignKey(Banner, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=get_tenant_specific_upload_folder, verbose_name=_('Banner Image'))
    content = models.TextField(verbose_name='Content')

    def __str__(self):
        return "{banner}".format(banner=self.banner.title)

    def get_absolute_url(self):
        return reverse('dashboard:dashboard_banners:slide-create', kwargs=dict(banner_id=self.banner.id))
