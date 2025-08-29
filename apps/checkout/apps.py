import oscar.apps.checkout.apps as apps
from oscar.core.loading import get_class

from apps.checkout.applicator import SurchargeApplicator


class CheckoutConfig(apps.CheckoutConfig):
    name = 'apps.checkout'
    surcharge_applicator_class = SurchargeApplicator

    def ready(self):
        super(CheckoutConfig, self).ready()
        self.payment_details_view = get_class('checkout.views', 'PaymentDetailsView')
