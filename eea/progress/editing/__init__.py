""" Main product initializer
"""
from zope.i18nmessageid.message import MessageFactory
#from eea.progress.editing import zmi

EEAMessageFactory = MessageFactory('eea')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

#zmi.initialize()
