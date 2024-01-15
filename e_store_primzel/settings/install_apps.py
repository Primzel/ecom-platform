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
    'oscar.apps.catalogue.reviews',
    'oscar.apps.basket',
    'oscar.apps.offer',
    'oscar.apps.order',
    'oscar.apps.search',
    'oscar.apps.voucher',
    'oscar.apps.wishlists',
    'apps.dashboard',
    'oscar.apps.dashboard.reports',
    'oscar.apps.dashboard.users',
    'oscar.apps.dashboard.orders',
    'apps.dashboard.catalogue',
    'oscar.apps.dashboard.offers',
    'oscar.apps.dashboard.ranges',
    'oscar.apps.dashboard.reviews',
    'oscar.apps.dashboard.vouchers',
    'oscar.apps.dashboard.communications',
    'oscar.apps.dashboard.shipping',
    'sorl.thumbnail',
    'colorfield',
    'oscar.apps.communication',
]+[
    # Primzel Apps
    'apps.dashboard.pages',
    'apps.dashboard.configurable_menu',
    'apps.checkout',
    'apps.shipping',
    'apps.dashboard.settings',
    'apps.payment',
    'apps.dashboard.dashboard_payment',
    'apps.dashboard.partners',
    'apps.partner',
    'apps.catalogue',
    'apps.dashboard.banners',
    'apps.customer',
    'primzel.global_signal_handler',
]

SHARED_APPS = [
    'django_tenants',
    'multitenancy',
    'django.contrib.sites',

    # everything below here is optional
    'widget_tweaks',
    'haystack',
    'treebeard',
    'django_tables2',
    'storages',
    # 'elasticsearchapm.contrib.django',
    'primzel.payment_gateways'
]

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

if settings.DEBUG:
    INSTALLED_APPS = INSTALLED_APPS + ['debug_toolbar', ]
