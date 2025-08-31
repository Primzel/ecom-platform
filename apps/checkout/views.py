import importlib
import logging

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse, NoReverseMatch
from django.utils.translation import gettext_lazy as _
from django_tenants.utils import get_model
from oscar.core.loading import get_class

from apps.checkout.applicator import SurchargeApplicator
from apps.payment.models import PaymentMethod

BillingAddress = get_model("order", "BillingAddress")
PaymentDetailsView = get_class("checkout.views", "PaymentDetailsView")
Source = get_model("payment", "Source")
SourceType = get_model("payment", "SourceType")

logger = logging.getLogger(__name__)


class PaymentDetailsView(PaymentDetailsView):

    def get_context_data(self, **kwargs):
        ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)
        payment_method = self.get_payment_method(self.request)
        payment_method_object = PaymentMethod.objects.get(pk=payment_method) if payment_method else None

        stripe_token = self.is_stripe_payment(self.request)
        paypal_object_str = self.is_paypal_payment(self.request)

        basket_surcharges = SurchargeApplicator(request=self.request).get_surcharges(basket=self.request.basket)

        ctx.update(dict(basket_surcharges=basket_surcharges))

        ctx.update(dict(
            payment_method=payment_method_object,
            stripe_token=stripe_token,
            paypal_object_str=paypal_object_str
        ))

        return ctx

    def get_payment_method(self, request):
        return request.POST.get('payment_method') or request.session.get('selected_payment_method')

    def set_selected_payment_method(self, request, payment_method):
        request.session['selected_payment_method'] = payment_method

    def set_paypal_object(self, request, paypal_object_str):
        request.session['paypal_object_str'] = paypal_object_str

    def set_stripe_token(self, request, stripe_token):
        request.session['stripe_token'] = stripe_token

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
        self.clean_session(request)
        return self.render_preview(request)

    def is_stripe_payment(self, request):
        return request.POST.get('stripe_token', False) or request.session.get('stripe_token', False)

    def is_paypal_payment(self, request):
        return request.POST.get('paypal_transaction_detail_object', False) or request.session.get('paypal_object_str',
                                                                                                  False)

    def render_preview(self, request, **kwargs):
        stripe_token = self.is_stripe_payment(request)
        self.set_stripe_token(request, stripe_token)

        paypal_object_str = self.is_paypal_payment(request)
        self.set_paypal_object(request, paypal_object_str)

        payment_method = self.get_payment_method(request)
        self.set_selected_payment_method(request, payment_method)

        return super(PaymentDetailsView, self).render_preview(request, **kwargs)

    def clean_session(self, request):
        try:
            del request.session['selected_payment_method']
        except KeyError:
            pass
        try:
            del request.session['stripe_token']
        except KeyError:
            pass
        try:
            del request.session['paypal_object_str']
        except KeyError:
            pass
    def handle_place_order_submission(self, request):
        response = super(PaymentDetailsView, self).handle_place_order_submission(request)
        payment_method = PaymentMethod.objects.get(pk=self.get_payment_method(request=self.request))

        self.clean_session(request)

        module = importlib.import_module(
            'primzel.payment_gateways.gateway.{gateway}.client'.format(gateway=payment_method.payment_gateway.slug))
        Client = getattr(module, 'Client')
        if hasattr(Client, 'redirect'):
            return Client.redirect(
                self.request,
                payment_method=payment_method,
                response=response,
                **self.build_submission()
            )
        return response

    def get_message_context(self, order, code=None):
        site = get_current_site(self.request)
        ctx = {
            'user': self.request.user,
            'order': order,
            'site': site,
            'lines': order.lines.all(),
            'request': self.request
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
