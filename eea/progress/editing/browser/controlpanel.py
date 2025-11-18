"""Editing progress controlpanel Plone 6"""

import logging

from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from eea.progress.editing.interfaces import IEditingProgressSettings

logger = logging.getLogger("eea.progress.editing")


class EditingProgressRegistryEditForm(RegistryEditForm):
    """Editing progress form"""

    schema = IEditingProgressSettings
    schema_prefix = "editing"
    label = "Editing progress"


class EditingProgressControlPanelFormWrapper(ControlPanelFormWrapper):
    """Editing progress wrapper"""

    form = EditingProgressRegistryEditForm
