from django import forms
from oscar.core.loading import get_model

Bankcard = get_model('payment', 'Bankcard')


class BankCardForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BankCardForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Bankcard
        fields = '__all__'
