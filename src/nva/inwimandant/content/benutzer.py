# -*- coding: utf-8 -*-
import re
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
from plone.dexterity.content import Item
from plone.supermodel import model
from z3c.form.interfaces import IEditForm
from plone.autoform import directives
from zope import schema
from zope.interface import implementer
from plone.indexer.decorator import indexer
from plone import api as ploneapi
from zope.interface import Invalid
from zope.interface import invariant
from z3c.form import validator

# from nva.inwimandant import _

def raiseUserErrorIfDouble(obj, event):
    """Check if a User already exists
    """
    other = ploneapi.user.get(username=obj.user_id)
    count = 0
    newid = obj.user_id
    while other:
        count = count + 1
        newid = "%s-%s" %(obj.user_id, count)
        other = ploneapi.user.get(username=newid)
    obj.user_id = newid
    return

def setLocalRoles(obj, event):
    obj.manage_addLocalRoles(obj.user_id, (u'Editor', u'Owner'))

def passwort_constraint(value):
    """Check if Passwort passt zur Passwort-Policy"""
    regex = re.compile('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,20}$')
    if not regex.match(value):
        raise Invalid(u'Bitte Passwort prüfen: 8-20 Zeichen, mind. eine Zahl, mind. ein Großbuchstabe, mind. ein Kleinbuchstabe.')
    return True

def email_constraint(value):
    regex = re.compile("""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""")
    if not regex.match(value):
        raise Invalid(u'Bitte prüfen Sie die eingegebene E-Mail-Adresse.')
    return True

def userid_constraint(value):
    user = ploneapi.user.get(userid=value)
    if user:
        raise Invalid(u"Die Benutzerid wurde bereits vergeben.")
    return True

class IBenutzer(model.Schema):
    """ Content-Type Interface fuer den INWI-Benutzer """

    title = schema.TextLine(title=u'Vollständiger Name', required=True)

    user_id = schema.TextLine(title=u'Anmeldename', 
                              description=u"Die Nutzung der E-Mail-Adresse oder einer eindeutigen, trägerindividuellen Benutzerkennung\
                                            wird empfohlen.",
                              constraint = userid_constraint,
                              required=True)

    email = schema.TextLine(title=u'E-Mail-Adresse', constraint=email_constraint, required=True)

    location = schema.TextLine(title=u"Dienstort oder Dienstsitz", required=False)

    directives.omitted(IEditForm, 'password')
    password = schema.TextLine(title=u'Passwort', 
                               description=u"Mindestens 8 Zeichen, 1 Großbuchstabe, 1 Kleinbuchstabe und eine Zahl müssen enthalten\
                               sein.", 
                               constraint=passwort_constraint, required=True)

    directives.omitted(IEditForm, 'password_repeat')
    password_repeat = schema.TextLine(title=u'Passwort wiederholen', required=True)

    biography = schema.Text(title=u'Vita des Benutzers', required=False)

    portrait = NamedBlobImage(title=u'Porträtbild', required=False)

    @invariant
    def password_invariant(data):
        if data.password != data.password_repeat:
            raise Invalid(u"Die eingegebenen Passworte stimmen leider nicht überein.")


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

