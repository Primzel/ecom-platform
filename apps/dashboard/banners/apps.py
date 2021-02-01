from django.urls import path
from django.utils.translation import gettext_lazy as _
from oscar.core.application import OscarDashboardConfig
from oscar.core.loading import get_class


class BannersConfig(OscarDashboardConfig):
    name = 'apps.dashboard.banners'
    verbose_name = _('Banners')
    namespace = 'banners'
    default_permissions = ['is_staff']

    def ready(self):
        self.banners_listing = get_class('dashboard.banners.views', 'BannerListView')
        self.banners_create = get_class('dashboard.banners.views', 'BannerCreateView')
        self.slide_create = get_class('dashboard.banners.views', 'SlideCreateView')
        self.slide_update = get_class('dashboard.banners.views', 'SlideUpdateView')

    def get_urls(self):
        urls = [
            path(r'', self.banners_listing.as_view(), name='banners-listing'),
            path(r'create/', self.banners_create.as_view(), name='banners-create'),
            path(r'<int:banner_id>/slide/', self.slide_create.as_view(), name='slide-create'),
            path(r'<int:banner_id>/slide/<int:pk>/update', self.slide_update.as_view(), name='slide-update'),
        ]
        return urls
