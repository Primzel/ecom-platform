from django import forms

from oscar.core.loading import get_model

Partner = get_model('partner', 'Partner')


class PartnerCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Partner.name and Partner.image are optional and that is okay. But if creating through
        # the dashboard, it seems sensible to enforce as it's the only field
        # in the form.
        self.fields['name'].required = True
        self.fields['image'].required = True

    class Meta:
        model = Partner
        fields = ('name', 'image')
