import stripe
from django.http import HttpResponse
from oscar.apps.order.models import PaymentEvent, Order


def ipn_callback(request,payment_method, *args, **kwargs):
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
        order = payment_intent.order
        oscar_order = Order.objects.get(number=order.number)
        payment_event = PaymentEvent(
            order=oscar_order,
            amount=payment_intent.amount,
            event_type_id=kwargs.get('payment_event_type_id'),
            reference=event.id
        )
        payment_event.save()

    else:
        # Unexpected event type
        return HttpResponse(status=400)

    return HttpResponse(status=200)