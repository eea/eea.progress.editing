""" Module where all interfaces, events and exceptions live.

    >>> portal = layer['portal']
    >>> sandbox = portal._getOb('sandbox')

"""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import Interface


class IBaseObject(Interface):
    """ Marker interface for Archetypes or Dexterity objects
    """


class IEEAEditingProgressLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IEditingProgress(Interface):
    """ Marker interface for editing
    """


class IEditingProgressState(Interface):
    """ Marker interface for editing state
    """


#
# Adapters
#

# add controlpanel entry with json editing progress taken from https://www.eea.europa.eu/portal_progress/ims-indicator
# have adapter compare progress with new cpanel entry.
# have restapi send progress from registry/adapter and then the Plone4 fallback