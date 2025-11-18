"""Module where all interfaces, events and exceptions live.

>>> portal = layer['portal']
>>> sandbox = portal._getOb('sandbox')

"""

try:
    from plone.schema import JSONField
except ImportError:
    from zope.schema import Dict as JSONField
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import Interface
from eea.progress.editing import EEAMessageFactory as _


class IBaseObject(Interface):
    """Marker interface for Archetypes or Dexterity objects"""


class IEEAEditingProgressLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IEditingProgress(Interface):
    """Marker interface for editing"""


class IEditingProgressState(Interface):
    """Marker interface for editing state"""


class IEditingProgressSettings(Interface):
    """Editing progress schema"""

    progress = JSONField(
        title=_("Progress"),
        description=_("Editing progress configuration"),
        required=False,
        default={},
        missing_value={},
    )
