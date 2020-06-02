import json

from django.http import HttpResponse
from oscar.apps.order.models import Order, PaymentEventType, PaymentEvent

from apps.payment.models import PaypalTransaction
from primzel.payment_gateways.gateway.paypal.enums import PaymentEventTypeEnum


def ipn_callback(request, payment_method, *args, **kwargs):
    payload = json.loads(request.body)['resource']

    paypal_transaction = PaypalTransaction.objects.get(reference=payload['id'])
    order = Order.objects.get(number=paypal_transaction.number)
    event_type, is_created = PaymentEventType.objects.get_or_create(
        code=PaymentEventTypeEnum.PAYMENT_CONFIRMED.name,
        name=PaymentEventTypeEnum.PAYMENT_CONFIRMED.value)
    payment_event = PaymentEvent(
        order=order,
        amount=payload['amount']['value'],
        event_type=event_type,
        reference=paypal_transaction.reference
    )
    payment_event.save()

    return HttpResponse(status=200)
