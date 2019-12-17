from oscar.core.loading import get_model
from treebeard.forms import movenodeform_factory
PartnerConfigurableMenu=get_model('configurable_menu','PartnerConfigurableMenu')
PartnerConfigurableMenuForm = movenodeform_factory(
    PartnerConfigurableMenu,
    fields=['title', 'site', 'is_primary'])