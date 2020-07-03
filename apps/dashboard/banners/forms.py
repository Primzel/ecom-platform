from django import forms
from oscar.core.loading import get_model
from treebeard.forms import movenodeform_factory

Banner = get_model('banners', 'Banner')
BannerImage = get_model('banners', 'BannerImage')


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = '__all__'


class SlideForm(forms.ModelForm):
    class Meta:
        model = BannerImage
        fields = '__all__'
