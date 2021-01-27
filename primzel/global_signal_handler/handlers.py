from django.core.cache import cache
from oscar.core.loading import get_model


def order_placed_handler(sender, order, user, *args, **kwargs):
    key = 'user__order_notes'
    message = cache.get(key, None)
    if message:
        OrderNote = get_model('order', 'OrderNote')
        OrderNote.objects.create(order=order, user=user, message=message, note_type=OrderNote.INFO)
        cache.delete(key)


def start_checkout_handler(sender, request, *args, **kwargs):
    key = 'user__order_notes'
    order_notes = request.GET.get('order_notes', None)
    if order_notes:
        cache.set(key, order_notes)
    else:
        cache.delete(key)
