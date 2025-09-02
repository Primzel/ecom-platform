from django.conf import settings

TENANT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',

    'oscar.config.Shop',
    'oscar.apps.analytics.apps.AnalyticsConfig',
    'oscar.apps.address.apps.AddressConfig',
    'oscar.apps.catalogue.reviews.apps.CatalogueReviewsConfig',
    'oscar.apps.basket.apps.BasketConfig',
    'oscar.apps.offer.apps.OfferConfig',
    'oscar.apps.order.apps.OrderConfig',
    'oscar.apps.search.apps.SearchConfig',
    'oscar.apps.voucher.apps.VoucherConfig',
    'oscar.apps.wishlists.apps.WishlistsConfig',
    'apps.dashboard.apps.DashboardConfig',
    'oscar.apps.dashboard.reports.apps.ReportsDashboardConfig',
    'oscar.apps.dashboard.users.apps.UsersDashboardConfig',
    'oscar.apps.dashboard.orders.apps.OrdersDashboardConfig',

    'apps.dashboard.catalogue',
    'oscar.apps.dashboard.offers.apps.OffersDashboardConfig',
    'oscar.apps.dashboard.ranges.apps.RangesDashboardConfig',
    'oscar.apps.dashboard.reviews.apps.ReviewsDashboardConfig',
    'oscar.apps.dashboard.vouchers.apps.VouchersDashboardConfig',
    'oscar.apps.dashboard.communications.apps.CommunicationsDashboardConfig',
    'oscar.apps.dashboard.shipping.apps.ShippingDashboardConfig',
    'sorl.thumbnail',
    'colorfield',
]

PRIMZEL_APPS = [
    # Primzel Apps
    'apps.communication.apps.CommunicationConfig',
    'apps.dashboard.pages',
    'apps.dashboard.configurable_menu.apps.ConfigurableMenuConfig',
    'apps.checkout',
    'apps.shipping',
    'apps.dashboard.settings',
    'apps.payment',
    'apps.dashboard.dashboard_payment.apps.PaymentDashboardConfig',
    'apps.dashboard.partners',
    'apps.partner',
    'apps.catalogue',
    'apps.dashboard.banners.apps.BannersConfig',
    'apps.customer',
    'primzel.global_signal_handler',
]

TENANT_APPS += PRIMZEL_APPS

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
