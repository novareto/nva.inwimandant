# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from zope.interface import Interface
from nva.inwimandant.content.benutzer import passwort_constraint
from Products.PluggableAuthService import interfaces
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import invariant
from zope import schema

class IInwiMandantPlugin(Interface):
    """Marker Interface"""

class INvaInwimandantLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""

class IChangePassword(Interface):
    """Form Fields for Change Password Form"""

    password = schema.Password(title=u'Passwort',
                               description=u"Mindestens 8 Zeichen, 1 Großbuchstabe, 1 Kleinbuchstabe und eine Zahl müssen enthalten\
                               sein.",
                               constraint=passwort_constraint, required=True)

    password_repeat = schema.Password(title=u'Passwort wiederholen', required=True)

    @invariant
    def password_invariant(data):
        if data.password != data.password_repeat:
            raise Invalid(u"Die eingegebenen Passworte stimmen leider nicht überein.")
