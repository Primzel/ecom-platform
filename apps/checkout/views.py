from django_tenants.utils import get_model
from oscar.core.loading import get_class

from apps.payment.models import PaymentMethod
from primzel.payment_gateways.gateway.stripe.client import StripeClient

BillingAddress = get_model("order", "BillingAddress")
PaymentDetailsView = get_class("checkout.views", "PaymentDetailsView")
Source = get_model("payment", "Source")
SourceType = get_model("payment", "SourceType")


class PaymentDetailsView(PaymentDetailsView):

    def get_context_data(self, **kwargs):
        ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)

        return ctx

    def get_payment_method(self, request):
        return request.POST.get('payment_method')

    def handle_payment(self, order_number, total, **kwargs):
        payment_method = PaymentMethod.objects.get(pk=self.get_payment_method(request=self.request))
        source_type, is_created = SourceType.objects.get_or_create(
            name=payment_method.title)
        stripe_token = self.is_stripe_payment(self.request)
        if stripe_token:
            source_type, is_created = SourceType.objects.get_or_create(
                name=payment_method.title)
            stripe_client = StripeClient(api_key=payment_method.secret_key)
            stripe_client.create_intent(stripe_token=stripe_token, amount=int(total.incl_tax * 1000),
                                        currency=total.currency)

        source = Source(
            source_type=source_type,
            currency=total.currency,
            amount_allocated=total.incl_tax,
            amount_debited=total.incl_tax

        )

        self.add_payment_source(source)

    def handle_payment_details_submission(self, request):
        return self.render_preview(request)

    def is_stripe_payment(self, request):
        return request.POST.get('stripe_token', False)

    def render_preview(self, request, **kwargs):
        stripe_token = self.is_stripe_payment(request)
        payment_method = self.get_payment_method(request)
        payment_method_object = PaymentMethod.objects.get(pk=payment_method)
        if stripe_token:
            kwargs.update(dict(stripe_token=stripe_token))
        kwargs.update(dict(payment_method=payment_method_object))
        return super(PaymentDetailsView, self).render_preview(request, **kwargs)
