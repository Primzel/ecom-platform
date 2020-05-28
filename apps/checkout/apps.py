import oscar.apps.checkout.apps as apps
from oscar.core.loading import get_class


class CheckoutConfig(apps.CheckoutConfig):
    name = 'apps.checkout'

    def ready(self):
        super(CheckoutConfig,self).ready()
        self.payment_details_view = get_class('checkout.views', 'PaymentDetailsView')
