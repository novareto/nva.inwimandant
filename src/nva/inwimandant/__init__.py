# -*- coding: utf-8 -*-
"""Init and utils."""
import install
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('nva.inwimandant')

install.register_inwimandant_plugin()

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    install.register_inwimandant_plugin_class(context)
