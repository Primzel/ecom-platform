"""e_store_primzel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.apps import apps
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from django.conf.urls import include, url  # < Django-2.0
from django.urls import include, path  # > Django-2.0
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from primzel.payment_gateways.views import IPNActionView

urlpatterns = [
    # url(r'^i18n/', include('django.conf.urls.i18n')),
    path('i18n/', include('django.conf.urls.i18n')),  # > Django-2.0

    # The Django admin is not officially supported; expect breakage.
    # Nonetheless, it's often useful for debugging.

    # url(r'^admin/', admin.site.urls),
    path('admin/', admin.site.urls),  # > Django-2.0

    # url(r'^', include(apps.get_app_config('oscar').urls[0])),
    path('', include(apps.get_app_config('oscar').urls[0])),  # > Django-2.0
    path('ipn/<str:gateway>/<int:payment_event_type_id>/<str:payment_method>/', csrf_exempt(IPNActionView.as_view())),
]
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    import debug_toolbar
    from django.urls import path

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),

                      # For django versions before 2.0:
                      # url(r'^__debug__/', include(debug_toolbar.urls)),

                  ] + urlpatterns
