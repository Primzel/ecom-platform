from django_tenants.utils import get_model
from oscar.apps.payment.forms import BillingAddressForm
from oscar.core.loading import get_class

BillingAddress = get_model("order", "BillingAddress")
PaymentDetailsView = get_class("checkout.views", "PaymentDetailsView")
Source = get_model("payment", "Source")
SourceType = get_model("payment", "SourceType")


class PaymentDetailsView(PaymentDetailsView):

    def get_context_data(self, **kwargs):
        ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)

        return ctx

    def handle_payment(self, order_number, total, **kwargs):
        source_type, is_created = SourceType.objects.get_or_create(
            name='Cash on Delivery')
        source = Source(
            source_type=source_type,
            currency=total.currency,
            amount_allocated=total.incl_tax,
            amount_debited=total.incl_tax
        )
        self.add_payment_source(source)
