from zope.interface import provider
from zope import schema

from Products.CMFCore.interfaces import ISiteRoot, IFolderish
from Products.statusmessages.interfaces import IStatusMessage

from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone import api as ploneapi

@provider(IContextSourceBinder)
def possible_groups(context):

    current = ploneapi.user.get_current()
    groups = ploneapi.group.get_groups(user=current)
    terms = []
    for i in groups:
        if i.id not in 'AuthenticatedUsers':
            terms.append(SimpleTerm(value=i.id, token=i.id, title=i.getGroupTitleOrName().decode('utf-8')))
    return SimpleVocabulary(terms)
