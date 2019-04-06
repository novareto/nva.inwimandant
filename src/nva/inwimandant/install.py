from AccessControl.Permissions import manage_users
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService import registerMultiPlugin

import plugin

manage_add_inwimandant_form = PageTemplateFile('browser/add_plugin',
                            globals(), __name__='manage_add_inwimandant_form' )


def manage_add_inwimandant_helper( dispatcher, id, title=None, REQUEST=None ):
    """Add an inwimandant Helper to the PluggableAuthentication Service."""

    sp = plugin.InwiMandant( id, title )
    dispatcher._setObject( sp.getId(), sp )

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect( '%s/manage_workspace'
                                      '?manage_tabs_message='
                                      'inwimandantHelper+added.'
                                      % dispatcher.absolute_url() )


def register_inwimandant_plugin():
    registerMultiPlugin(plugin.InwiMandant.meta_type)


def register_inwimandant_plugin_class(context):
    context.registerClass(plugin.InwiMandant,
                          permission = manage_users,
                          constructors = (manage_add_inwimandant_form,
                                          manage_add_inwimandant_helper),
                          visibility = None,
                          icon='browser/icon.gif'
                         )
