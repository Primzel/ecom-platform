from split_settings.tools import include, optional

from .logging import *
from .base import *
from .install_apps import *
from .celery import *
from .templates import *
from .database import *
from .middleware import *
from .navigation import *
from .application_defination import *
from .multitenant import *
from .aws import *
from .apm import *

include(
    optional('env/local.py'),
    scope=locals()
)
