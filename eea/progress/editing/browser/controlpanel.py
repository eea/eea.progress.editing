""" Editing progress controlpanel Plone 6
"""
import json
import logging

from plone import schema
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import Interface

try:
    from plone.schema import JSONField
except ImportError:
    pass


logger = logging.getLogger("eea.progress.editing")

VOCABULARY_SCHEMA = json.dumps(
    {}
)


class IEditingProgressSettings(Interface):
    progress = schema.JSONField(
        title="Progress",
        description="Editing progress configuration",
        required=False,
        schema=VOCABULARY_SCHEMA,
        default={},
        missing_value={},
    )


class EditingProgressRegistryEditForm(RegistryEditForm):
    schema = IEditingProgressSettings
    schema_prefix = "editing"
    label = "Editing progress Settings"


class EditingProgressControlPanelFormWrapper(ControlPanelFormWrapper):
    form = EditingProgressRegistryEditForm


@adapter(Interface, Interface)
class EditingProgressRegistryConfigletPanel(RegistryConfigletPanel):
    """Volto control panel"""

    schema = IEditingProgressSettings
    schema_prefix = "editing"
    configlet_id = "editingprogress-controlpanel"
    configlet_category_id = "Products"
    title = "Editing Progress Settings"
    group = "Products"