import json

from oscar.apps.payment.models import SourceType

from apps.payment.models import PaypalTransaction


class Client():
    @classmethod
    def get_paypal_transaction_object(cls, request):
        return json.loads(request.POST.get('paypal_object_str'))

    @classmethod
    def handle_payment(cls, request, view, total, payment_method, *args, **kwargs):
        source_type, is_created = SourceType.objects.get_or_create(name=payment_method.title)
        payload = cls.get_paypal_transaction_object(request)
        for purchase_unit in payload['purchase_units']:
            for capture in purchase_unit['payments']['captures']:
                PaypalTransaction.objects.create(reference=capture['id'], status=capture['status'],
                                                 number=kwargs.get('order_number'))
        return source_type, is_created
