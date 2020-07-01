from django.db import models
from django.utils.translation import gettext_lazy as _
from oscar.apps.partner.abstract_models import AbstractPartner

class Partner(AbstractPartner):
    image = models.ImageField(_('Image'), upload_to='partner_image', blank=True,
                              null=True, max_length=255)


from oscar.apps.partner.models import *  # noqa isort:skip