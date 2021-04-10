from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from oscar.apps.dashboard.pages.views import (
    PageCreateView as OscarPageCreateView,
    PageUpdateView as OscarPageUpdateView,
    PageCreateUpdateMixin as OscarPageCreateUpdateMixin
)


class PageCreateUpdateMixin(OscarPageCreateUpdateMixin):
    def form_valid(self, form):
        # Ensure saved page is added to the current site
        page = form.save()
        if not page.sites.exists():
            page.sites.add(Site.objects.get_current(self.request))
        self.object = page
        return HttpResponseRedirect(self.get_success_url())


class PageCreateView(OscarPageCreateView, PageCreateUpdateMixin):
    pass


class PageUpdateView(OscarPageUpdateView, PageCreateUpdateMixin):
    pass
