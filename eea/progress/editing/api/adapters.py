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
        self._done = 100

    @property
    def steps(self):
        """Return a SimpleVocabulary like tuple with progress fields as dicts:

        (
          {
           'is_ready': 'Boolean if field ready or not',
           'label': 'Message of progress field'
           'icon': 'Field icon if valid or invalid'
           'link': 'Field href to edit',
           'link_label': 'Field href message'
           }
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
                field_dict = {'is_ready': is_ready}
                if is_ready:
                    field_dict['label'] = wview.get('labelReady')
                    field_dict['icon'] = wview.get('iconReady')
                    field_dict['link'] = ''
                    field_dict['link_label'] = ''
                else:
                    field_dict['label'] = wview.get('labelEmpty')
                    field_dict['icon'] = wview.get('iconEmpty')
                    field_dict['link'] = wview.ctx_url + wview.get('link')
                    field_dict['link_label'] = wview.get('linkLabel')
                self._steps.append(field_dict)
            # progressbar/browser/app/view.py#L155
            # progress is set correctly only after call to schema() from
            # progress.metadata browserview otherwise we get the 100 fallback
            # as such we set the done value here instead of within the property
            self._done = mview.progress

        return self._steps

    @property
    def done(self):
        """Done"""
        return self._done
