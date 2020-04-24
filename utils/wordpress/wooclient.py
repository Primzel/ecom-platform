from woocommerce import API


class WooClient():
    def __init__(self, url, consumer_key, consumer_secret, version="wc/v3", timeout=60):
        self.wcapi = API(
            url=url,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            version=version,
            timeout=timeout
        )

    def get(self, endpoint, **kwargs):
        return self.wcapi.get(endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.wcapi.post(endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self.wcapi.put(endpoint, **kwargs)
