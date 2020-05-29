import os

from .base import BASE_DIR

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # templates directory of the project
        ],
        'OPTIONS': {
            'loaders': [
                "django_tenants.template.loaders.filesystem.Loader",  # Must be first
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',

                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.customer.notifications.context_processors.notifications',
                'oscar.core.context_processors.metadata',
                'apps.dashboard.settings.context_processors.store',
            ],
        },
    },
]

MULTITENANT_TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, 'templates/%s/templates')
]
