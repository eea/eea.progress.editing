# pylint: disable = C0412
""" Editing progress controlpanel Plone 6
"""
import logging

from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper, \
    RegistryEditForm
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import Interface

try:
    from plone.schema import JSONField
except ImportError:
    from zope.schema import Dict as JSONField


logger = logging.getLogger("eea.progress.editing")


class IEditingProgressSettings(Interface):
    """ Editing progress schema """

    progress = JSONField(
        title="Progress",
        description="Editing progress configuration",
        required=False,
        default={},
        missing_value={},
    )


class EditingProgressRegistryEditForm(RegistryEditForm):
    """ Editing progress form """
    schema = IEditingProgressSettings
    schema_prefix = "editing"
    label = "Editing progress Settings"


class EditingProgressControlPanelFormWrapper(ControlPanelFormWrapper):
    """ Editing progress wrapper """
    form = EditingProgressRegistryEditForm


@adapter(Interface, Interface)
class EditingProgressRegistryConfigletPanel(RegistryConfigletPanel):
    """ Volto control panel """

    schema = IEditingProgressSettings
    schema_prefix = "editing"
    configlet_id = "editingprogress-controlpanel"
    configlet_category_id = "Products"
    title = "Editing Progress Settings"
    group = "Products"
