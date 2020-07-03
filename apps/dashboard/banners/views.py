# Create your views here.
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django_tables2 import SingleTableView
from oscar.core.loading import get_class, get_model

from apps.dashboard.banners.forms import BannerForm, SlideForm

BannerTable = get_class('dashboard.banners.tables', 'BannerTable')
Banner = get_model('banners', 'Banner')
BannerImage = get_model('banners', 'BannerImage')


class BannerCreateView(generic.CreateView):
    template_name = 'banners/dashboard/create-banners.html'
    model = Banner
    form_class = BannerForm

    def get_form_kwargs(self):
        kwargs = super(BannerCreateView, self).get_form_kwargs()
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super(BannerCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _("Add a new banner")
        return ctx


class BannerListView(SingleTableView):
    table_class = BannerTable
    context_object_name = 'table'
    template_name = 'banners/dashboard/banner-listing.html'
    queryset = Banner.objects.all()

    def get_queryset(self, **kwargs):
        qs = super(BannerListView, self).get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super(BannerListView, self).get_context_data(**kwargs)
        ctx['title'] = _("Banners")
        return ctx


class SlideCreateView(generic.CreateView):
    template_name = 'banners/dashboard/slide-form.html'
    model = BannerImage
    form_class = SlideForm

    def get_context_data(self, **kwargs):
        ctx = super(SlideCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _("Add a new slide")
        ctx['banner'] = Banner.objects.get(pk=self.kwargs.get('banner_id', None))
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Slide created successfully"))
        return super().get_success_url()

    def get_initial(self):
        initial = super().get_initial()
        initial['banner'] = self.kwargs.get('banner_id', None)
        return initial
