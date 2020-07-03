import oscar.apps.dashboard.apps as apps
from django.apps import apps as django_apps
from django.conf.urls import include, url


class DashboardConfig(apps.DashboardConfig):
    name = 'apps.dashboard'

    def ready(self):
        super(DashboardConfig, self).ready()
        self.configurable_menu_app = django_apps.get_app_config('configurable_menu')
        self.dashboard_payment_app = django_apps.get_app_config('dashboard_payment')
        self.dashboard_banners_app = django_apps.get_app_config('banners')

    def get_urls(self):
        from django.contrib.auth import views as auth_views
        from django.contrib.auth.forms import AuthenticationForm
        urls = [
            url(r'^$', self.index_view.as_view(), name='index'),
            url(r'^catalogue/', include(self.catalogue_app.urls[0])),
            url(r'^reports/', include(self.reports_app.urls[0])),
            url(r'^orders/', include(self.orders_app.urls[0])),
            url(r'^users/', include(self.users_app.urls[0])),
            url(r'^pages/', include(self.pages_app.urls[0])),
            url(r'^partners/', include(self.partners_app.urls[0])),
            url(r'^offers/', include(self.offers_app.urls[0])),
            url(r'^ranges/', include(self.ranges_app.urls[0])),
            url(r'^reviews/', include(self.reviews_app.urls[0])),
            url(r'^vouchers/', include(self.vouchers_app.urls[0])),
            url(r'^comms/', include(self.comms_app.urls[0])),
            url(r'^shipping/', include(self.shipping_app.urls[0])),
            url(r'^partner-configurable-menu/',
                include((self.configurable_menu_app.urls[0], 'configurable_menu'), namespace='configurable_menu')),
            url(r'^payment/',
                include((self.dashboard_payment_app.urls[0], 'dashboard_payment'), namespace='dashboard_payment')),
            url(r'^login/$',
                auth_views.LoginView.as_view(template_name='oscar/dashboard/login.html',
                                             authentication_form=AuthenticationForm),
                name='login'),
            url(r'^logout/$', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
            url(r'^banners/',
                include((self.dashboard_banners_app.urls[0], 'dashboard_banners'), namespace='dashboard_banners')),
        ]
        return self.post_process_urls(urls)
