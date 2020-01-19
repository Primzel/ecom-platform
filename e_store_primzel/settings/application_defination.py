# Application definition
import os

ROOT_URLCONF = os.getenv('PRIMZEL_ROOT_URLCONF','e_store_primzel.urls')

WSGI_APPLICATION = os.getenv('PRIMZEL_WSGI_APPLICATION','e_store_primzel.wsgi.application')