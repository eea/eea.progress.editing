"""Controlpanel API"""

from zope.interface import Interface
from zope.component import adapter
from plone.restapi.controlpanels import RegistryConfigletPanel
from eea.progress.editing.interfaces import IEEAEditingProgressLayer
from eea.progress.editing.interfaces import IEditingProgressSettings


@adapter(Interface, IEEAEditingProgressLayer)
class Controlpanel(RegistryConfigletPanel):
    """Control Panel"""

    schema = IEditingProgressSettings
    schema_prefix = "editing"
    configlet_id = "eea.progress.editing"
    configlet_category_id = "Products"
    title = "Editing Progress"
    group = "Products"
