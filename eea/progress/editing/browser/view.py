"""Editing progress browser views"""

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from zope.component import queryMultiAdapter, queryUtility
from plone.memoize.view import memoize

try:
    from eea.progressbar.interfaces import IProgressTool
except ImportError:

    class IProgressTool(object):
        """Fallback"""

        pass


class EditingProgressView(BrowserView):
    """Editing progress"""

    @memoize
    def state_is_ready(self):
        """Check if every field is ready for current state"""

        tool = queryUtility(IProgressTool)
        ctype = getattr(self.context, "portal_type", {})
        ctype = tool.get(ctype)
        if not ctype:
            return True
        wftool = getToolByName(self.context, "portal_workflow")
        state = wftool.getInfoFor(self.context, "review_state")
        self.request.ctx = self.context
        config = queryMultiAdapter((ctype, self.request), name="view")
        for field in config.schema():
            widget = config.view(field)
            states = [term.value for term in widget.workflow()]
            if "all" not in states:
                if state not in states:
                    continue

            ready = widget.ready(self.context)
            if not ready:
                return False
        return True
