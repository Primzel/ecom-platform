import os

from crequest.middleware import CrequestMiddleware
from django.contrib.sites.models import Site
from django.template import TemplateDoesNotExist, Template, Origin
from django.template.loaders.base import Loader
import logging

logger = logging.getLogger(__name__)


class CustomTemplateLoader(Loader):
    def get_template_sources(self, template_name):
        """
        An iterator that yields possible matching template paths for a
        template name.
        """
        yield Origin(
            name=template_name,
            template_name=template_name,
            loader=self,
        )

    def get_contents(self, origin):
        try:
            from django.conf import settings
            current_request = CrequestMiddleware.get_request()
            try:
                current_site = Site.objects.get(domain=current_request.get_host())
            except Site.DoesNotExist:
                current_site = Site.objects.get(id=settings.DEFAULT_SITE_ID)
            absolute_path = '{app_template_directory}/{partner_template_dir}/{template_name}'.format(
                template_name=origin.name,
                partner_template_dir=current_site.name,
                app_template_directory=
                origin.loader.engine.dirs[0]
            )
            content = open(
                absolute_path
            ).read()
            logger.info(absolute_path,extra=dict(template_name=origin.name,
                             partner_template_dir=current_site.name,
                             app_template_directory=origin.loader.engine.dirs))
            return content
        except FileNotFoundError:
            raise TemplateDoesNotExist(origin)
