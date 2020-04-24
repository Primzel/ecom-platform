from .wooclient import WooClient


class Client():
    def __init__(self, *args, **kwargs):
        self.client = WooClient(**kwargs)

    def get_products(self, **kwargs):
        return self.client.get('products', **kwargs)

    def get_categories(self, **kwargs):
        return self.client.get('products/categories', **kwargs)

    def create_product(self, payload):
        return self.client.post('products', data=payload)

    def update_product(self, payload, id):
        return self.client.put('products/%s' % id, data=payload)
