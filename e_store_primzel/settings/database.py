# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB_NAME', 'primzel_store'),
        'USER': os.getenv('POSTGRES_USER', 'primzel_store'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'primzel_store'),
        'HOST': os.getenv('POSTGRES_HOST', 'psql.primzel.com'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}