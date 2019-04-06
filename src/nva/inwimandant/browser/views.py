from Acquisition import aq_inner
from plone import api as ploneapi
from Products.Five import BrowserView
from nva.inwimandant.vocabularies import possible_groups


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
            userlist.append(entry)
        return userlist


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
