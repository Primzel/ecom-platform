import importlib

from django import views

from apps.payment.models import PaymentMethod


# Create your views here.


class IPNActionView(views.View):
    def post(self, request, *args, **kwargs):
        payment_method = PaymentMethod.objects.get(pk=kwargs.pop('payment_method'))
        module = importlib.import_module(
            'primzel.payment_gateways.gateway.{gateway}.action'.format(gateway=payment_method.payment_gateway.slug))
        ipn_callback = getattr(module, 'ipn_callback')
        return ipn_callback(request, payment_method, *args, **kwargs)
