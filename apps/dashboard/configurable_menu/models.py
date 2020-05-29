from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.
from oscar.apps.catalogue.abstract_models import AbstractCategory


class PartnerConfigurableMenu(models.Model):
    title = models.CharField(max_length=250)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{title} {status}".format(title=self.title,
                                               status=' (primary)' if self.is_primary else '')

    def get_absolute_url(self):
        return reverse('dashboard:configurable_menu:partner-configurable-menu-create')


class PartnerConfigurableMenuItem(AbstractCategory):
    category = models.ManyToManyField(
        'catalogue.Category', related_name="partner_menu_items",
        blank=True, verbose_name=_("Categories"))
    patner_menu = models.ForeignKey('PartnerConfigurableMenu', related_name='menu', on_delete=models.CASCADE)

    included_categories = models.ManyToManyField(
        'catalogue.Category', related_name='menu_includes', blank=True,
        verbose_name=_("Included Categories"))

    class Meta:
        abstract = False
        app_label = 'configurable_menu'
        ordering = ['name']
        verbose_name = _("Configurable MenuItem")
        verbose_name_plural = _("Configurable MenuItems")
