# -*- coding: utf-8 -*-
# Copyright (c) 2007-2019 NovaReto GmbH
# lwalther@novareto.de
from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from OFS.Cache import Cacheable
from plone import api as ploneapi
from zope.interface import implementer
from nva.inwimandant.interfaces import IInwiMandantPlugin
from Products.PluggableAuthService.interfaces import plugins as pas_interfaces
import logging

logger = logging.getLogger('event.InwiMandantPlugin')
zmidir = os.path.join(os.path.dirname(__file__), "zmi")

def manage_addInwiPlugin(dispatcher, id, title="", RESPONSE=None, **kw):
    """Create an instance of a Inwi Plugin.
    """
    inwiplugin = InwiMandant(id, title, **kw)
    dispatcher._setObject(inwiplugin.getId(), inwiplugin)
    if RESPONSE is not None:
        RESPONSE.redirect("manage_workspace")


manage_addInwiPluginForm = PageTemplateFile(
    os.path.join(zmidir, "add_plugin.pt"), globals(), __name__="addInwiPlugin"
)

@implementer(
    IInwiMandantPlugin,
    pas_interfaces.IAuthenticationPlugin,
    pas_interfaces.IGroupsPlugin,
    pas_interfaces.IPropertiesPlugin,
    pas_interfaces.IUserEnumerationPlugin,
)
class InwiMandant(BasePlugin, Cacheable):
    """Multi-plugin
    """

    meta_type = 'InwiMandant'
    security = ClassSecurityInfo()
    _dont_swallow_my_exceptions = True

    manage_options = ( ( { 'label': 'Users',
                           'action': 'manage_users', }
                         ,
                       )
                     + BasePlugin.manage_options
                     + Cacheable.manage_options
                     )

    def __init__( self, id, title=None ):
        self._setId( id )
        self.title = title

    security.declarePrivate('authenticateCredentials')
    def authenticateCredentials(self, credentials):
        login = credentials.get( 'login' )
        password = credentials.get( 'password' )
        if login is None or password is None:
            return None
        user = ploneapi.content.find(portal_type='Benutzer', mandant_userid=login)
        if not user:
            return None
        logged = user[0].getObject()
        if logged.password == password:
            return (login, login)
        return None

    security.declarePrivate('getPropertiesForUser')
    def getPropertiesForUser(self, user, request=None):
        if user:
            userid = user.getUserId()
            try:
                userbrains = ploneapi.content.find(portal_type='Benutzer', mandant_userid=userid)
            except:
                print('Error in encoding')
                userbrains = []
            if userbrains:
                logged = userbrains[0].getObject()
                mydict = {}
                mydict['fullname'] = logged.title
                mydict['email'] = logged.email
                if logged.location:
                    mydict['location'] = logged.location
                if logged.biography:
                    mydict['description'] = logged.biography
                return mydict
        return dict() 
        
    security.declarePrivate('enumerateUsers')
    def enumerateUsers(self, id=None, login=None, exact_match=False,
            sort_by=None, max_results=None, **kw):

        key = login or id

        mylist = []
        if key:
            users = ploneapi.content.find(portal_type='Benutzer', mandant_userid=key)
            for i in users:
	        mylist.append({
                               "id" : i.mandant_userid,
                               "login" : i.mandant_userid,
                               "pluginid" : self.getId(),
                              })
        if kw.get('fullname'):
            users = ploneapi.content.find(portal_type='Benutzer', Title=kw.get('fullname'))
            for i in users:
                mylist.append({"id": i.mandant_userid,
                               "login": i.mandant_userid,
                               "pluginid" : self.getId(),})

        elif kw.get('email'):
            users = ploneapi.content.find(portal_type='Benutzer', mandant_email=kw.get('email'))
            for i in users:
                mylist.append({"id": i.mandant_userid,
                               "login": i.mandant_userid,
                               "pluginid" : self.getId(),})
        elif kw.get('name'):
            users = ploneapi.content.find(portal_type='Benutzer', mandant_userid=kw.get('name'))
            for i in users:
                mylist.append({"id": i.mandant_userid,
                               "login": i.mandant_userid,
                               "pluginid" : self.getId(),})
        return mylist
	
    security.declarePrivate('getGroupsForPrincipal')
    def getGroupsForPrincipal(self, principal, request=None, attr=None):
        if not request:
            return ()
        if not principal:
            return ()
        if principal:
            try:
                users = ploneapi.content.find(portal_type='Benutzer', mandant_userid=principal.getUserId())
                if users:
                    userobj = users[0].getObject()
                    return (userobj.aq_parent.group,)
            except:
                return ()
        return ()
            
InitializeClass(InwiMandant)
