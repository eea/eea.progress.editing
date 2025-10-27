"""GET"""

# -*- coding: utf-8 -*-
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.services import Service
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import adapter, queryAdapter
from zope.interface import implementer
from zope.interface import Interface
from eea.progress.editing.interfaces import IEditingProgress


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class EditingProgress(object):
    """Get editing progress"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        result = {
            "editing.progress": {
                "@id": "{}/@editing.progress".format(self.context.absolute_url())
            }
        }
        if not expand:
            return result

        if IPloneSiteRoot.providedBy(self.context):
            return result

        progress = queryAdapter(self.context, IEditingProgress)
        if progress:
            result["editing.progress"]["steps"] = json_compatible(progress.steps)
        result["editing.progress"]["done"] = json_compatible(progress.done)
        return result


class EditingProgressGet(Service):
    """Get editing progress information"""

    def reply(self):
        """Reply"""
        info = EditingProgress(self.context, self.request)
        return info(expand=True)["editing.progress"]
