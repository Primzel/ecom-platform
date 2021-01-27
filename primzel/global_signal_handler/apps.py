from django.apps import AppConfig
from oscar.apps.checkout.signals import start_checkout
from oscar.apps.order.signals import order_placed

from primzel.global_signal_handler.handlers import order_placed_handler, start_checkout_handler


class GlobalSignalHandlerConfig(AppConfig):
    name = 'primzel.global_signal_handler'

    def ready(self):
        order_placed.connect(order_placed_handler)
        start_checkout.connect(start_checkout_handler)
