from django.contrib import admin

# Register your models here.
from apps.dashboard.banners.models import Banner, BannerImage

admin.site.register(Banner)
admin.site.register(BannerImage)