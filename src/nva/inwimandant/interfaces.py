# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from Products.PluggableAuthService import interfaces
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class INvaInwimandantLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""

class IInwiMandant(interfaces.plugins.IAuthenticationPlugin,
                   interfaces.plugins.IExtractionPlugin,
                   interfaces.plugins.IRolesPlugin,
                   interfaces.plugins.IPropertiesPlugin,
                   interfaces.plugins.IGroupsPlugin,
                   interfaces.plugins.IUserEnumerationPlugin):
    """interface for InwiGroupHelper."""
