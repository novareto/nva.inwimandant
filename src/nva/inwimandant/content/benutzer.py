# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.dexterity.content import Item
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


# from nva.inwimandant import _


class IBenutzer(model.Schema):
    """ Content-Type Interface fuer den INWI-Benutzer """

    title = schema.TextLine(title=u'Vollständiger Name', required=True)

    user_id = schema.TextLine(title=u'Anmeldename', required=True)

    email = schema.TextLine(title=u'E-Mail-Adresse', required=True)

    password = schema.Password(title=u'Passwort', required=True)

    password_repeat = schema.Password(title=u'Passwort wiederholen', required=True)

    biography = RichText(title=u'Vita des Benutzers', required=False)


@implementer(IBenutzer)
class Benutzer(Item):
    """
    """
