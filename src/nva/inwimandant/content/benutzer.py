# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
from plone.dexterity.content import Item
from plone.supermodel import model
from zope import schema
from zope.interface import implementer
from plone.indexer.decorator import indexer


# from nva.inwimandant import _


class IBenutzer(model.Schema):
    """ Content-Type Interface fuer den INWI-Benutzer """

    title = schema.TextLine(title=u'Vollständiger Name', required=True)

    user_id = schema.TextLine(title=u'Anmeldename', required=True)

    email = schema.TextLine(title=u'E-Mail-Adresse', required=True)

    location = schema.TextLine(title=u"Dienstort oder Dienstsitz", required=False)

    password = schema.Password(title=u'Passwort', required=True)

    password_repeat = schema.Password(title=u'Passwort wiederholen', required=True)

    biography = schema.Text(title=u'Vita des Benutzers', required=False)

    portrait = NamedBlobImage(title=u'Porträtbild', required=False)


@implementer(IBenutzer)
class Benutzer(Item):
    """
    """

@indexer(IBenutzer)
def mandant_userid(object, **kw):
     return object.user_id

@indexer(IBenutzer)
def mandant_email(object, **kw):
     return object.email

