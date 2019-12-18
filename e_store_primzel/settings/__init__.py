from .logging import *
from .base import *
from .celery import *
from .templates import *
from .database import *
from .middleware import *
from .install_apps import *
from .navigation import *
from split_settings.tools import include, optional

include(
    optional('env/local.py'),
    scope=locals()
)
