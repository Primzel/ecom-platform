import importlib
import logging

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse, NoReverseMatch
from django.utils.translation import gettext_lazy as _
from django_tenants.utils import get_model
from oscar.core.loading import get_class

from apps.payment.models import PaymentMethod

BillingAddress = get_model("order", "BillingAddress")
PaymentDetailsView = get_class("checkout.views", "PaymentDetailsView")
Source = get_model("payment", "Source")
SourceType = get_model("payment", "SourceType")

logger = logging.getLogger(__name__)


class PaymentDetailsView(PaymentDetailsView):

    def get_context_data(self, **kwargs):
        ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)

        return ctx

    def get_payment_method(self, request):
        return request.POST.get('payment_method')

    def handle_payment(self, order_number, total, **kwargs):
        payment_method = PaymentMethod.objects.get(pk=self.get_payment_method(request=self.request))

        module = importlib.import_module(
            'primzel.payment_gateways.gateway.{gateway}.client'.format(gateway=payment_method.payment_gateway.slug))
        Client = getattr(module, 'Client')

        source_type, is_created = Client.handle_payment(self.request, self, total, payment_method,
                                                        order_number=order_number)

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

    def is_paypal_payment(self, request):
        return request.POST.get('paypal_transaction_detail_object', False)

    def render_preview(self, request, **kwargs):
        stripe_token = self.is_stripe_payment(request)
        payment_method = self.get_payment_method(request)
        paypal_object_str = self.is_paypal_payment(request)
        try:
            payment_method_object = PaymentMethod.objects.get(pk=payment_method)
            kwargs.update(dict(payment_method=payment_method_object, stripe_token=stripe_token,
                               paypal_object_str=paypal_object_str))
        except ValueError as e:
            messages.error(
                self.request,
                _("Please select payment gateway "
                  "back to the checkout process"))
            logger.error(e)
        return super(PaymentDetailsView, self).render_preview(request, **kwargs)

    def handle_place_order_submission(self, request):

        return super(PaymentDetailsView, self).handle_place_order_submission(request)

    def get_message_context(self, order, code=None):
        site=get_current_site(self.request)
        ctx = {
            'user': self.request.user,
            'order': order,
            'site': site,
            'lines': order.lines.all()
        }

        # Attempt to add the order status URL to the email template ctx.
        try:
            if self.request.user.is_authenticated:
                path = reverse('customer:order',
                               kwargs={'order_number': order.number})
            else:
                path = reverse('customer:anon-order',
                               kwargs={'order_number': order.number,
                                       'hash': order.verification_hash()})
        except NoReverseMatch:
            # We don't care that much if we can't resolve the URL
            pass
        else:
            ctx['status_url'] = 'http://%s%s' % (site.domain, path)
        return ctx
