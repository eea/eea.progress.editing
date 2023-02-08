""" Progress adapters
"""
from plone import api
from eea.progress.editing.interfaces import IEditingProgress
from zope.interface import implementer


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
        # (Pdb) mview.__class__
        # <class 'Products.Five.metaclass.SimpleViewClass from /plone/instance/src/eea.progressbar/eea/progressbar/browser/zpt/metadata.pt'>
        mview = self.context.restrictedTraverse('@@progress.metadata', None)
        if mview:
            # Plone 4
            widgets_views = list(mview.schema())
            for wview in widgets_views:
                # (Pdb) pp vars(wview)
                # {'_condition': 'Test',
                # '_custom': None,
                # '_hidden': False,
                # '_ready': 'Test',
                # '_workflow': [<zope.schema.vocabulary.SimpleTerm object at 0x7f8f16a68310>],
                # 'context': <Article at /www/portal_progress/article/.schema>,
                # 'ctx_url': 'http://10.110.30.235:55427/www/SITE/sandbox/petchesi-iulian-eau-de-web/test/',
                # 'field': <Field title(string:rw)>,
                # 'label': 'Title',
                # 'parent': <ProgressContentType at /www/portal_progress/article>,
                # 'prefix': 'title',
                # 'request': <HTTPRequest, URL=http://10.110.30.235:55427/www/SITE/sandbox/petchesi-iulian-eau-de-web/test/@editing.progress>}

                # (Pdb) wview.ready.__code__
                # <code object ready at 0x7f8f3b582830, file "/plone/instance/src/eea.progressbar/eea/progressbar/widgets/simple/view.py", line 55>


                is_ready = True if wview.ready() else False
                field_dict = {'is_ready': is_ready,
                              'states': wview.get('states')}
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
        else:
            # Plone 6
            registry_record = api.portal.get_registry_record('editing.progress')
            ptype = self.context.portal_type
            ptype_record = registry_record.get(ptype, [])

            for record in ptype_record:
                pass
                # check and compare record to the context
                # return results


        return self._steps

    @property
    def done(self):
        """Done"""
        return self._done
