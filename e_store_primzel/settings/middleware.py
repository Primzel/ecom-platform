from django.conf import settings

MIDDLEWARE = [
    'elasticapm.contrib.django.middleware.TracingMiddleware',
    'django_tenants.middleware.main.TenantMainMiddleware',
    'middlewares.multitenancy.TenantTemplatesMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'crequest.middleware.CrequestMiddleware',
    'middlewares.logging.HeadersLoggingMiddleware',
]

if settings.DEBUG:
    MIDDLEWARE = MIDDLEWARE + [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
