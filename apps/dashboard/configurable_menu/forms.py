from django import forms
from oscar.core.loading import get_model

# from treebeard.forms import movenodeform_factory

PartnerConfigurableMenu = get_model('configurable_menu', 'PartnerConfigurableMenu')
Partner = get_model('partner', 'Partner')


# PartnerConfigurableMenuForm = movenodeform_factory(
#     PartnerConfigurableMenu,
#     fields=['title', 'site', 'is_primary'])

class PartnerConfigurableMenuForm(forms.ModelForm):
    partner = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PartnerConfigurableMenuForm, self).__init__(*args, **kwargs)
        self.fields['partner'].queryset = Partner.objects.all() if user.is_superuser else user.partners

    class Meta:
        model = PartnerConfigurableMenu
        fields = '__all__'
