""" GET
"""
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
    """ Get editing progress
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        result = {"editing.progress": {
            "@id": "{}/@editing.progress".format(self.context.absolute_url())
        }}
        if not expand:
            return result

        if IPloneSiteRoot.providedBy(self.context):
            return result

        progress = queryAdapter(self.context, IEditingProgress)
        if progress:
            result["editing.progress"]['steps'] = json_compatible(
                progress.steps)
        result["editing.progress"]['done'] = json_compatible(
            progress.done)
        return result

# progress.steps =
# [
#  {'icon': u'eea-icon eea-icon-edit',
#   'is_ready': False,
#   'label': u'Please set the PDF cover main image of this Article',
#   'link': u'http://10.110.30.235:55427/www/SITE/sandbox/petchesi-iulian-eau-de-web/test/edit#fieldsetlegend-default',
#   'link_label': u'Add PDF cover main image',
#   'states': [u'all']},
#  {'icon': u'eea-icon eea-icon-edit',
#   'is_ready': False,
#   'label': u'Please set the Exclude from Table of Contents of this Article',
#   'link': u'http://10.110.30.235:55427/www/SITE/sandbox/petchesi-iulian-eau-de-web/test/edit#fieldsetlegend-default',
#   'link_label': u'Add Exclude from Table of Contents',
#   'states': [u'all']},
#  {'icon': u'eea-icon eea-icon-check',
#   'is_ready': True,
#   'label': u'You added the Table of contents depth level',
#   'link': '',
#   'link_label': '',
#   'states': [u'all']}]


class EditingProgressGet(Service):
    """Get editing progress information"""

    def reply(self):
        """ Reply
        """
        info = EditingProgress(self.context, self.request)
        return info(expand=True)["editing.progress"]
