from zope.interface import Interface
from Acquisition import aq_inner
from plone import api as ploneapi
from Products.Five import BrowserView
from nva.inwimandant.vocabularies import possible_groups
from uvc.api import api


class BenutzerOrdnerView(BrowserView):
    """View fuer den Benutzerordner"""

    def get_group(self):
        group = ploneapi.group.get(groupname=self.context.group)
        return group.getGroupTitleOrName().decode('utf-8')

    def get_userlist(self):
        fc = self.context.getFolderContents()
        userlist = []
        for i in fc:
            entry = {}
            entry['titel'] = i.Title
            entry['username'] = i.mandant_userid
            entry['url'] = i.getURL()
            entry['changelink'] = self.changelink(i.getURL())
            userlist.append(entry)
        return userlist

    def changelink(self, entryurl):
        link = ''
        current = ploneapi.user.get_current()
        if self.context.getOwner().getId() == current.getId():
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


class ManageChangePassword(api.View):
    api.context(Interface)

    def render(self):
        userid = ploneapi.user.get_current().getId()
        mandantuser = ploneapi.content.find(portal_type="Benutzer", mandant_userid=userid)
        if mandantuser:
            url = mandantuser[0].getURL() + '/@@changepasswordform'
            return self.redirect(url)
        return


class IsMandantUser(api.View):
    api.context(Interface)

    def render(self):
        userid = ploneapi.user.get_current().getId()
        mandantuser = ploneapi.content.find(portal_type="Benutzer", mandant_userid=userid)
        if mandantuser:
            return True
        return False

class isFolderOwner(api.View):
    api.context(Interface)

    def render(self):
        import pdb;pdb.set_trace()
