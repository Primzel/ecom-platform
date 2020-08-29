from django import template
from oscar.core.loading import get_model

register = template.Library()
Partner = get_model("partner", "Partner")


@register.simple_tag(name="partners")  # noqa: C901 too complex
def get_partner_list(offset=0, limit=10):
    partners = Partner.objects.all()
    if offset >= 0 and limit >= 0:
        partners=partners[offset:limit]
    return partners
