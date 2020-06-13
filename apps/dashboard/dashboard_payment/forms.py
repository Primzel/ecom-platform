from django import forms
from oscar.core.loading import get_model

Bankcard = get_model('payment', 'Bankcard')
Source = get_model('payment', 'Source')
SourceType = get_model('payment', 'SourceType')
Transaction = get_model('payment', 'Transaction')
PaymentMethod = get_model('payment', 'PaymentMethod')
AvailablePaymentGateway = get_model('payment_gateways', 'AvailablePaymentGateway')


class BankCardForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BankCardForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Bankcard
        fields = '__all__'


class SourceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SourceForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Source
        fields = '__all__'


class SourceTypeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SourceTypeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = SourceType
        fields = '__all__'


class TransactionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Transaction
        fields = '__all__'


class PaymentMethodForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PaymentMethodForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PaymentMethod
        fields = '__all__'


class AvailablePaymentGatewayForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = AvailablePaymentGateway
        fields = '__all__'
