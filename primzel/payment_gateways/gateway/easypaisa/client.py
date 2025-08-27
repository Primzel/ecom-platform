import base64
import hashlib
import hmac

from django.shortcuts import render
from oscar.apps.order.models import Order

from apps.payment.models import SourceType


def sign_value(value, signing_secret_key):
    signature = hmac.new(
        signing_secret_key.encode('utf-8'),
        value.encode('utf-8'),
        hashlib.sha256
    ).digest()
    return base64.b64encode(signature).decode('utf-8')


class Client():
    @classmethod
    def redirect(self, request, payment_method, basket, *args, **kwargs):
        oscar_order = Order.objects.get(basket=basket)
        base_url = request.build_absolute_uri('/')[:-1]
        context = {
            'form_action': 'https://easypay.easypaisa.com.pk/easypay/Index.jsf',
            'form_data': {
                'orderRefNum': oscar_order.number,
                'storeId': payment_method.publishable_key,
                'amount': int(oscar_order.total_incl_tax),
                'postBackURL': f'{base_url}/checkout/thank-you/#',
                'autoRedirect': 1,
                'emailAddr': request.user.email if request.user.is_authenticated else '',
                'paymentMethod':'CC_PAYMENT_METHOD',
            }
        }
        context['form_data']['merchantHashedReq'] = sign_value(
            f"amount={context['form_data']['amount']}&emailAddr={context['form_data']['emailAddr']}&"
            f"orderRefNum={context['form_data']['orderRefNum']}&postBackURL={context['form_data']['postBackURL']}&"
            f"storeId={context['form_data']['storeId']}",
            payment_method.signing_secret_key
        )


        return render(request, 'oscar/checkout/partials/auto_post_form.html', context)

    @classmethod
    def handle_payment(cls, request, view, total, payment_method, *args, **kwargs):
        source_type, is_created = SourceType.objects.get_or_create(name=payment_method.title)
        return source_type, is_created
