# -*- coding: utf-8 -*-
# Copyright (c) 2007-2019 NovaReto GmbH
# lwalther@novareto.de
from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements
from OFS.Folder import Folder
from OFS.Cache import Cacheable
from Products.PluggableAuthService.interfaces.plugins import \
    IAuthenticationPlugin, IUserEnumerationPlugin, IGroupsPlugin

import interfaces

from base64 import encodestring, decodestring
from urllib import quote, unquote
from plone import api as ploneapi

import logging

logger = logging.getLogger('event.InwiMandantPlugin')


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

#    security.declarePrivate('getRolesForPrincipal')
#    def getRolesForPrincipal( self, principal, request=None ):
#        if not request:
#            return ()
#        return ['Member',]

    security.declarePrivate('getPropertiesForUser')
    def getPropertiesForUser(self, user, request=None):
        if user:
            userid = user.getUserId()
            userbrains = ploneapi.content.find(portal_type='Benutzer', mandant_userid=userid)
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
            users = ploneapi.content.find(portal_type='Benutzer', mandant_userid=principal.getUserId())
            if users:
                userobj = users[0].getObject()
                return (userobj.aq_parent.group,)
        return ()
            
#    def extractCredentials(self, request):
#        return 

classImplements(InwiMandant, interfaces.IInwiMandant)
InitializeClass(InwiMandant)

