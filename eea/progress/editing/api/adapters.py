"""Progress adapters"""

from logging import getLogger
from plone.api import portal

from Acquisition import ImplicitAcquisitionWrapper
from eea.progress.editing.interfaces import IEditingProgress
from plone.restapi.services.sources.get import get_field_by_name
from zope.interface import implementer
from zope.pagetemplate.engine import TrustedEngine, TrustedZopeContext


logger = getLogger("eea.progress.editing")


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
        mview = self.context.restrictedTraverse("@@progress.metadata", None)
        if mview:
            # Plone 4
            widgets_views = list(mview.schema())
            for wview in widgets_views:
                is_ready = True if wview.ready() else False
                field_dict = {"is_ready": is_ready, "states": wview.get("states")}
                if is_ready:
                    field_dict["label"] = wview.get("labelReady")
                    field_dict["icon"] = wview.get("iconReady")
                    field_dict["link"] = ""
                    field_dict["link_label"] = ""
                else:
                    field_dict["label"] = wview.get("labelEmpty")
                    field_dict["icon"] = wview.get("iconEmpty")
                    field_dict["link"] = wview.ctx_url + wview.get("link")
                    field_dict["link_label"] = wview.get("linkLabel")
                self._steps.append(field_dict)
            # progressbar/browser/app/view.py#L155
            # progress is set correctly only after call to schema() from
            # progress.metadata browserview otherwise we get the 100 fallback
            # as such we set the done value here instead of within the property
            self._done = mview.progress
        else:
            # Plone 6
            registry_record = portal.get_registry_record("editing.progress")
            ptype = self.context.portal_type
            ptype_record = registry_record.get(ptype, [])

            for record in ptype_record:
                is_ready = True if self.condition(record) else False
                field_dict = {
                    "is_ready": is_ready,
                    "states": self.get(record, "states"),
                }

                if is_ready:
                    field_dict["label"] = self.get(record, "labelReady")
                    field_dict["icon"] = self.get(record, "iconReady")
                    field_dict["link"] = ""
                    field_dict["link_label"] = ""
                else:
                    field_dict["label"] = self.get(record, "labelEmpty")
                    field_dict["icon"] = self.get(record, "iconEmpty")
                    field_dict["link"] = "%s/%s" % (
                        self.context.absolute_url(),
                        self.get(record, "link"),
                    )
                    field_dict["link_label"] = self.get(record, "linkLabel")

                self._steps.append(field_dict)
                # custom method for done/progress
        return self._steps

    def get(self, record, name, default=""):
        """Get record property"""
        value = record.get(name, default)
        if isinstance(value, str):
            prefix = record.get("prefix")
            field = get_field_by_name(prefix, self.context)
            label = getattr(field, "title", prefix)
            widget = getattr(field, "widget", None)
            value = value.format(
                label=label, field=field, context=self.context, widget=widget
            )
        return value

    def condition(self, record):
        """condition custom method"""
        context = self.context
        condition = record.get("condition")
        field = get_field_by_name(record.get("prefix"), context)
        value = (
            field.get(context)
            if field
            else getattr(context, record.get("prefix"), None)
        )  # noqa
        engine = TrustedEngine
        zopeContext = TrustedZopeContext(
            engine,
            {
                "context": context,
                "request": self.context.REQUEST,
                "field": field,
                "value": value,
            },
        )

        try:
            expression = engine.compile(condition)
            result = zopeContext.evaluate(expression)
        except Exception as err:
            logger.exception(err)
            result = False

        if callable(result) and not isinstance(result, ImplicitAcquisitionWrapper):  # noqa
            result = result()

        return result

    @property
    def done(self):
        """Done"""
        return self._done
