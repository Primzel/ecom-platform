import stripe
from django.conf import settings


class StripeClient():
    def __init__(self, api_key, stripe_version="2020-03-02"):
        self.api_key, self.stripe_version = api_key, stripe_version

    def charge(self, idempotency_key, amount, currency, source):
        return stripe.Charge.create(
            api_key=self.api_key,
            stripe_version=self.stripe_version,
            amount=amount,
            currency=currency,
            idempotency_key=idempotency_key,
            source=idempotency_key,
            description="My First Test Charge (created for API docs)",
        )

    def create_intent(self, stripe_token, amount, currency):
        return stripe.Charge.create(source=stripe_token, api_key=self.api_key, stripe_version=self.stripe_version,
                                    currency=currency, amount=amount)
