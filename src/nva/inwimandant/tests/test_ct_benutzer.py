# -*- coding: utf-8 -*-
from nva.inwimandant.content.benutzer import IBenutzer  # NOQA E501
from nva.inwimandant.testing import NVA_INWIMANDANT_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class BenutzerIntegrationTest(unittest.TestCase):

    layer = NVA_INWIMANDANT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            'Benutzerordner',
            self.portal,
            'benutzer',
            title='Parent container',
        )
        self.parent = self.portal[parent_id]

    def test_ct_benutzer_schema(self):
        fti = queryUtility(IDexterityFTI, name='Benutzer')
        schema = fti.lookupSchema()
        self.assertEqual(IBenutzer, schema)

    def test_ct_benutzer_fti(self):
        fti = queryUtility(IDexterityFTI, name='Benutzer')
        self.assertTrue(fti)

    def test_ct_benutzer_factory(self):
        fti = queryUtility(IDexterityFTI, name='Benutzer')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IBenutzer.providedBy(obj),
            u'IBenutzer not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_benutzer_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.parent,
            type='Benutzer',
            id='benutzer',
        )

        self.assertTrue(
            IBenutzer.providedBy(obj),
            u'IBenutzer not provided by {0}!'.format(
                obj.id,
            ),
        )

    def test_ct_benutzer_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Benutzer')
        self.assertFalse(
            fti.global_allow,
            u'{0} is globally addable!'.format(fti.id)
        )
