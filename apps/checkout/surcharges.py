from oscar.apps.checkout.surcharges import FlatCharge


class FlatCharge(FlatCharge):
    def __init__(self, name, code, excl_tax=None, incl_tax=None):
        super().__init__(excl_tax=excl_tax, incl_tax=incl_tax)
        self.name = name
        self.code = code
