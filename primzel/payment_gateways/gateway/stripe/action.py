import stripe
from django.http import HttpResponse
from oscar.apps.order.models import PaymentEvent, Order, PaymentEventType

from primzel.payment_gateways.gateway.stripe.enums import PaymentEventTypeEnum


def ipn_callback(request, payment_method, *args, **kwargs):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, payment_method.signing_secret_key, api_key=payment_method.publishable_key)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'charge.succeeded':
        payment_intent = event.data.object  # contains a stripe.PaymentIntent
        metadata = payment_intent.metadata
        event_type, is_created = PaymentEventType.objects.get_or_create(
            code=PaymentEventTypeEnum.PAYMENT_CONFIRMED.name,
            name=PaymentEventTypeEnum.PAYMENT_CONFIRMED.value)
        oscar_order = Order.objects.get(basket__id=metadata.basket_id)
        payment_event = PaymentEvent(
            order=oscar_order,
            amount=payment_intent.amount / payment_method.currency_factory,
            event_type=event_type,
            reference=event.id
        )
        payment_event.save()

    else:
        # Unexpected event type
        return HttpResponse(status=400)

    return HttpResponse(status=200)
