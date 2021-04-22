""" Module where all interfaces, events and exceptions live.

    >>> portal = layer['portal']
    >>> sandbox = portal._getOb('sandbox')

"""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import Interface


class IBaseObject(Interface):
    """ Marker interface for Archetypes or Dexterity objects
    """


class IEEAProgressEditingLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IProgressEditing(Interface):
    """ Marker interface for editing
    """


class IProgressEditingState(Interface):
    """ Marker interface for editing state
    """


#
# Adapters
#
