""" Progress adapters
"""
from zope.interface import implementer
from eea.progress.editing.interfaces import IEditingProgress


@implementer(IEditingProgress)
class EditingProgress(object):
    """
    Abstract adapter for editing progress. This will be used as a fallback
    adapter if the API can't find a more specific adapter for your editing

    """

    def __init__(self, context):
        self.context = context
        self._steps = None
        self._done = 0

    @property
    def steps(self):
        """Return a SimpleVocabulary like tuple with progress fields info:

        (
          ('Boolean if field ready or not',
          'Field icon if valid or invalid', 'Message of progress field',
          'Field href to edit', 'Field href text'
          )
        )

        """
        if self._steps is not None:
            return self._steps

        self._steps = []
        mview = self.context.restrictedTraverse('@@progress.metadata', None)
        if mview:
            widgets_views = list(mview.schema())
            for wview in widgets_views:
                is_ready = True if wview.ready() else False
                if is_ready:
                    label = wview.get('labelReady')
                    icon = wview.get('iconReady')
                    link = ''
                    link_label = ''
                else:
                    label = wview.get('labelEmpty')
                    icon = wview.get('iconEmpty')
                    link = wview.ctx_url + wview.get('link')
                    link_label = wview.get('linkLabel')
                self._steps.append([is_ready, label, icon, link,
                                    link_label])
            self._done = mview.progress

        return self._steps

    @property
    def done(self):
        """Done"""
        return self._done

