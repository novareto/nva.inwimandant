# -*- coding: utf-8 -*-
from AccessControl.Permissions import add_user_folders
from nva.inwimandant.plugin import InwiMandant
from nva.inwimandant.plugin import manage_addInwiPlugin
from nva.inwimandant.plugin import manage_addInwiPluginForm
from nva.inwimandant.plugin import zmidir
from Products.PluggableAuthService import registerMultiPlugin
from zope.i18nmessageid import MessageFactory

import os

_ = MessageFactory('nva.inwimandant')

def initialize(context):
    registerMultiPlugin(InwiMandant.meta_type)
    context.registerClass(
        InwiMandant,
        permission=add_user_folders,
        icon=os.path.join(zmidir, "inwi_user.png"),
        constructors=(manage_addInwiPluginForm, manage_addInwiPlugin),
        visibility=None,
    )
