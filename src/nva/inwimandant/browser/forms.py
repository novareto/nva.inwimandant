# -*- coding:utf-8 -*-
from nva.inwimandant.interfaces import IChangePassword
from z3c.form import button, form
import plone.z3cform.layout
from plone.autoform.form import AutoExtensibleForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as FiveViewPageTemplateFile
from plone import api as ploneapi

class ChangePasswordForm(AutoExtensibleForm, form.Form):

    label = u"Änderung des Passwortes"
    description = u""

    ignoreContext = True
    schema = IChangePassword
    output = None

    def checkowner(self):
        userid = ploneapi.user.get_current().getId()
        if userid == self.context.user_id:
            return True
        if self.context.aq_inner.aq_parent.getOwner().getId() == userid:
            return True
        if self.context.aq_inner.aq_parent.Creator() == userid:
            if "Editor" in ploneapi.user.get_roles(username=userid, obj=self.context):
                return True
        if userid in self.context.aq_inner.aq_parent.Contributors():
            if "Editor" in ploneapi.user.get_roles(username=userid, obj=self.context):
                return True
        return False

    def update(self):
        super(ChangePasswordForm, self).update()
        message = u"Sie haben keine Berechtigung zum Ändern des Kennwortes."
        if not self.checkowner():
            ploneapi.portal.show_message(message=message, request=self.request, type="error")
            url = ploneapi.portal.get().absolute_url()
            return self.redirect(url)
        self.formurl = self.context.absolute_url() + '/changepasswordform'

    @button.buttonAndHandler("Neues Password speichern")
    def save_password(self):
        data, errors = self.extractData()
        if errors:
            ploneapi.portal.show_message(message='Bitte korrigieren Sie die angezeigten Fehler.',
                                         request=self.request, type="error")
            return
        message = u"Ihr Passwort wurde erfolgreich geändert."
        self.context.password = data.get('password')
        ploneapi.portal.show_message(message=message, request=self.request, type="info")
        url = ploneapi.portal.get().absolute_url()
        return self.redirect(url)

    @button.buttonAndHandler('Abbrechen')
    def handel_cancel(self):
        url = ploneapi.portal.get().absolute_url()
        return self.redirect(url)

changepasswordform = plone.z3cform.layout.wrap_form(ChangePasswordForm, index=FiveViewPageTemplateFile("changepasswordform.pt"))    
