from .base import *
from .celery import *
from .templates import *
from split_settings.tools import include, optional

include(
    optional('env/local.py'),
    scope=locals()
)
