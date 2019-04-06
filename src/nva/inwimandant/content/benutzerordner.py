# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer
from nva.inwimandant.vocabularies import possible_groups

# from nva.inwimandant import _

class IBenutzerordner(model.Schema):
    """ Content-Type Interface fuer Benutzerordner
    """

    group = schema.Choice(title=u"Auswahl der Gruppe für die Benutzer angelegt werden sollen",
                          source=possible_groups,
                          required=True)

@implementer(IBenutzerordner)
class Benutzerordner(Container):
    """
    """
