import logging

from django import template
from django.template.loader import select_template

from apps.dashboard.banners.models import Banner

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag(takes_context=True)
def render_banner(context, banner_slug):
    banner = False
    try:
        banner = Banner.objects.prefetch_related('images').get(slug=banner_slug)
    except Exception as e:
        logger.debug("Please define banner with slug = {slug}".format(slug=banner_slug))
    names = ['banners/banner.html']

    template_ = select_template(names)
    context = context.flatten()
    context['banner'] = banner
    return template_.render(context)
