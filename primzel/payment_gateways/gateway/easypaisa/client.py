from django.shortcuts import render
from oscar.apps.order.models import Order

from apps.payment.models import SourceType


class Client():
    @classmethod
    def redirect(self, request, basket, order_total, *args, **kwargs):
        oscar_order = Order.objects.get(basket=basket)

        context = {
            'form_action': 'https://easypay.easypaisa.com.pk/easypay/Index.jsf',
            'form_data': {
                'orderRefNum': oscar_order.number,
                'storeId': '6834',
                'amount': order_total,
                'postBackURL': 'localhost:8081/checkout/payment-details/?',
                'autoRedirect': 1,
                'emailAddr': request.user.email if request.user.is_authenticated else '',
            }
        }

        return render(request, 'oscar/checkout/partials/auto_post_form.html', context)

    @classmethod
    def handle_payment(cls, request, view, total, payment_method, *args, **kwargs):
        source_type, is_created = SourceType.objects.get_or_create(name=payment_method.title)
        return source_type, is_created
