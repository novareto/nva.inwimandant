from zope.interface import Interface
from Acquisition import aq_inner
from plone import api as ploneapi
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from nva.inwimandant.vocabularies import possible_groups

mailbody = """\
Guten Tag %s,

Ihnen wurde ein Zugang zum Portal https://dsm.siguv.de eingerichtet.

Benutzername:%s
Passwort:%s

Bitte ändern Sie das Passwort nach Ihrer ersten Anmeldung."""

class BenutzerOrdnerView(BrowserView):
    """View fuer den Benutzerordner"""

    def get_group(self):
        group = ploneapi.group.get(groupname=self.context.group)
        return group.getGroupTitleOrName()

    def get_userlist(self):
        fc = self.context.listFolderContents()
        userlist = []
        for i in fc:
            entry = {}
            entry['titel'] = i.title
            entry['username'] = i.user_id
            entry['url'] = i.absolute_url()
            entry['changelink'] = self.changelink(i.absolute_url())
            entry['mailto'] = self.get_mailto(i)
            userlist.append(entry)
        return userlist

    def get_mailto(self, user):
        mailbody = """\
Guten Tag %s,

Ihnen wurde ein Zugang zum Portal https://dsm.siguv.de eingerichtet.

Benutzer: %s
Passwort: %s

Bitte ändern Sie das Passwort nach Ihrer ersten Anmeldung.""" % (user.title, user.user_id, user.password)
        mailtolink = "mailto:%s?subject=Zugang zum Portal Datenschutzmanagement&body=%s" % (user.email, mailbody)
        return mailtolink

    def changelink(self, entryurl):
        link = ''
        current = ploneapi.user.get_current()
        userid = current.getId()
        if self.context.getOwner().getId() == userid:
            link = entryurl + '/@@changepasswordform'
        if self.context.Creator() == userid:
            if "Editor" in ploneapi.user.get_roles(username=userid, obj=self.context):
                link = entryurl + '/@@changepasswordform'
        if current.getId() in self.context.Contributors():
            if "Editor" in ploneapi.user.get_roles(username=userid, obj=self.context):
                link = entryurl + '/@@changepasswordform'
        return link
 
class BenutzerView(BrowserView):
    """View fuer den Benutzer"""

    def get_password(self):
        retpw = ""
        for i in self.context.password:
            retpw += "*"
        return retpw

    def get_portrait(self):
        if self.context.portrait:
            return "%s/@@images/portrait/thumb" %self.context.absolute_url()
        return ""


class ManageChangePassword(BrowserView):

    def __call__(self):
        userid = ploneapi.user.get_current().getId()
        mandantuser = ploneapi.content.find(portal_type="Benutzer", mandant_userid=userid)
        if mandantuser:
            url = mandantuser[0].getURL() + '/@@changepasswordform'
            return self.request.response.redirect(url)
        return


class IsMandantUser(BrowserView):

    def __call__(self):
        userid = ploneapi.user.get_current().getId()
        mandantuser = ploneapi.content.find(portal_type="Benutzer", mandant_userid=userid)
        if mandantuser:
            return True
        return False


class IsLocalUser(BrowserView):

    def __call__(self):
        userid = ploneapi.user.get_current().getId()
        acl_users = getToolByName(self.context, 'acl_users')
        source_users = acl_users.get('source_users')
        userids = [i.getId() for i in source_users.getUsers()]
        if userid in userids:
            return True
        return False


class IsExternalLogin(BrowserView):

    def __call__(self):
        return True

class IsMandantTest(BrowserView):

    def __call__(self):
        import pdb;pdb.set_trace()
