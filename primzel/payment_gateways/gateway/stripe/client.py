import stripe

from apps.payment.models import SourceType


class Client():
    def __init__(self, stripe_version="2020-03-02", *args, **kwargs):
        self.api_key, self.stripe_version = kwargs.get('api_key'), stripe_version

    def charge(self, idempotency_key, amount, currency, source):
        return stripe.Charge.create(
            api_key=self.api_key,
            stripe_version=self.stripe_version,
            amount=amount,
            currency=currency,
            idempotency_key=idempotency_key,
            source=idempotency_key,
        )

    def create_intent(self, stripe_token, amount, currency):
        return stripe.Charge.create(source=stripe_token, api_key=self.api_key, stripe_version=self.stripe_version,
                                    currency=currency, amount=amount)

    @classmethod
    def handle_payment(cls, request, view, total, payment_method, *args, **kwargs):
        stripe_token = view.is_stripe_payment(request)
        source_type, is_created = SourceType.objects.get_or_create(name=payment_method.title)
        stripe_client = Client(**dict(api_key=payment_method.secret_key))
        stripe_client.create_intent(stripe_token=stripe_token,
                                    amount=int(total.incl_tax * payment_method.currency_factory),
                                    currency=total.currency)
        return source_type, is_created
