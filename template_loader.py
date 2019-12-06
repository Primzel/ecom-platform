import os

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
            absolute_path = '{app_template_directory}/{partner_template_dir}/{template_name}'.format(
                template_name=origin.name,
                partner_template_dir=settings.site_name,
                app_template_directory=
                origin.loader.engine.dirs[
                    0])
            content = open(
                absolute_path
            ).read()
            logger.info(absolute_path)
            return content
        except FileNotFoundError:
            raise TemplateDoesNotExist(origin)
