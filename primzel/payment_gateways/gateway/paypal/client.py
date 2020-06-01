from oscar.apps.payment.models import SourceType


class Client():
    @classmethod
    def handle_payment(cls, request, view, total, payment_method, *args, **kwargs):
        source_type, is_created = SourceType.objects.get_or_create(name=payment_method.title)
        return source_type, is_created