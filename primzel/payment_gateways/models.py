from django.db import models


# Create your models here.
class AvailablePaymentGateway(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=300)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
