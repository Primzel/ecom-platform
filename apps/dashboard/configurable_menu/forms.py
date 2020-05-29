from django import forms
from oscar.core.loading import get_model

from treebeard.forms import movenodeform_factory

PartnerConfigurableMenu = get_model('configurable_menu', 'PartnerConfigurableMenu')
PartnerConfigurableMenuItem = get_model('configurable_menu', 'PartnerConfigurableMenuItem')

_PartnerMenuItemForm = movenodeform_factory(
    PartnerConfigurableMenuItem,
    fields=['name', 'description', 'image', 'patner_menu', 'included_categories'])


class PartnerMenuItemForm(_PartnerMenuItemForm):
    def __init__(self, *args, **kwargs):
        super(PartnerMenuItemForm, self).__init__(*args, **kwargs)


class PartnerConfigurableMenuForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PartnerConfigurableMenuForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PartnerConfigurableMenu
        fields = '__all__'
