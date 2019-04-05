# -*- coding: utf-8 -*-
from nva.inwimandant.content.benutzerordner import IBenutzerordner  # NOQA E501
from nva.inwimandant.testing import NVA_INWIMANDANT_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class BenutzerordnerIntegrationTest(unittest.TestCase):

    layer = NVA_INWIMANDANT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_ct_benutzerordner_schema(self):
        fti = queryUtility(IDexterityFTI, name='Benutzerordner')
        schema = fti.lookupSchema()
        self.assertEqual(IBenutzerordner, schema)

    def test_ct_benutzerordner_fti(self):
        fti = queryUtility(IDexterityFTI, name='Benutzerordner')
        self.assertTrue(fti)

    def test_ct_benutzerordner_factory(self):
        fti = queryUtility(IDexterityFTI, name='Benutzerordner')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IBenutzerordner.providedBy(obj),
            u'IBenutzerordner not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_benutzerordner_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Benutzerordner',
            id='benutzerordner',
        )

        self.assertTrue(
            IBenutzerordner.providedBy(obj),
            u'IBenutzerordner not provided by {0}!'.format(
                obj.id,
            ),
        )

    def test_ct_benutzerordner_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Benutzerordner')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_benutzerordner_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Benutzerordner')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'benutzerordner_id',
            title='Benutzerordner container',
         )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
