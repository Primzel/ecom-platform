from decimal import Decimal as D

from oscar.apps.checkout import applicator

from apps.checkout.surcharges import FlatCharge


class SurchargeApplicator(applicator.SurchargeApplicator):
    def __init__(self, request=None, context=None):
        super().__init__(request=request, context=context)

    def get_payment_method(self):
        return self.request.POST.get('payment_method')

    def get_surcharges(self, basket, **kwargs):
        from apps.payment.models import PaymentMethod

        try:
            payment_method = PaymentMethod.objects.get(pk=self.get_payment_method())
        except PaymentMethod.DoesNotExist:
            return ()
        if not payment_method or payment_method.charges <= 0:
            return ()
        return (
            FlatCharge(
                name=payment_method.title,
                code=payment_method.payment_gateway.slug,
                excl_tax=D(payment_method.charges * payment_method.currency_factory),
                incl_tax=D(payment_method.charges * payment_method.currency_factory)
            ),
        )
