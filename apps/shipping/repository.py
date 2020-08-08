from oscar.apps.shipping import repository
from oscar.core.loading import get_model

OrderAndItemCharges = get_model('shipping', 'OrderAndItemCharges')


class Repository(repository.Repository):
    @property
    def methods(self):
        return OrderAndItemCharges.objects.all()
