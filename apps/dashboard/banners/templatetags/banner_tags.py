from django import template
from django.template.loader import select_template

from apps.dashboard.banners.models import Banner

register = template.Library()


@register.simple_tag(takes_context=True)
def render_banner(context, banner_slug):
    banner = Banner.objects.prefetch_related('images').get(slug=banner_slug)
    names = ['banners/banner.html']

    template_ = select_template(names)
    context = context.flatten()
    context['banner'] = banner
    return template_.render(context)
