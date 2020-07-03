from django.conf import settings

TENANT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'oscar',
    'oscar.apps.analytics',
    'oscar.apps.address',
    'oscar.apps.shipping',
    'oscar.apps.catalogue.reviews',
    'oscar.apps.basket',
    'oscar.apps.offer',
    'oscar.apps.order',
    'oscar.apps.customer',
    'oscar.apps.search',
    'oscar.apps.voucher',
    'oscar.apps.wishlists',
    'apps.dashboard',
    'oscar.apps.dashboard.reports',
    'oscar.apps.dashboard.users',
    'oscar.apps.dashboard.orders',
    'apps.dashboard.catalogue',
    'oscar.apps.dashboard.offers',
    'oscar.apps.dashboard.pages',
    'oscar.apps.dashboard.ranges',
    'oscar.apps.dashboard.reviews',
    'oscar.apps.dashboard.vouchers',
    'oscar.apps.dashboard.communications',
    'oscar.apps.dashboard.shipping',
    'sorl.thumbnail',
]+[
    # Primzel Apps
    'apps.dashboard.configurable_menu',
    'apps.checkout',
    'apps.dashboard.settings',
    'apps.payment',
    'apps.dashboard.dashboard_payment',
    'apps.dashboard.partners',
    'apps.partner',
    'apps.catalogue',
    'apps.dashboard.banners'
]

SHARED_APPS = [
    'django_tenants',
    'multitenancy',
    'django.contrib.sites',

    # everything below here is optional
    'jet',
    'widget_tweaks',
    'haystack',
    'treebeard',
    'django_tables2',
    'storages',
    'elasticapm.contrib.django',
    'primzel.payment_gateways'
]

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

if settings.DEBUG:
    INSTALLED_APPS = INSTALLED_APPS + ['debug_toolbar', ]
