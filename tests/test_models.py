#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-rockpile
------------

Tests for `django-rockpile` modules module.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rockpile import models


class BasicProjectMixin(object):

    def setUp(self):
        self.user = User.objects.create_user(username='john', email='john_doe@fake.com', password='top_secret')
        self.owner = models.Owner.objects.create(user=self.user)
        self.translator = models.Translator.objects.create(user=self.user)
        self.translation_project = models.TranslationProject.objects.create(name='Test project', owner=self.owner)
        self.translation = models.Translation.objects.create(project=self.translation_project, language='es')
        self.translation.translators.add(self.translator)
        self.translation.save()


class FewStringsProjectMixin(BasicProjectMixin):

    def setUp(self):
        super(FewStringsProjectMixin, self).setUp()

        # Translated strings
        self.main_string1 = models.TranslatedString.objects.create(value='Hello world', translation=self.translation)
        self.translated_string1 = models.TranslatedString.objects.create(key=self.main_string1, value='Hola mundo',
                                                                         translation=self.translation, validated_by=self.translator)
        self.main_string2 = models.TranslatedString.objects.create(value='Testing string', translation=self.translation)
        self.translated_string2 = models.TranslatedString.objects.create(key=self.main_string2, value='Probando cadena',
                                                                         translation=self.translation)


class TestTranslationEmptyStrings(BasicProjectMixin, TestCase):

    def test_percentage_completion(self):
        self.assertEqual(self.translation.percentage_completed, 0.0)


class TestTranslation(FewStringsProjectMixin, TestCase):

    def test_percentage_completion(self):
        self.assertEqual(self.translation.percentage_completed, 50.0)


class TestTranslatedString(FewStringsProjectMixin, TestCase):

    def test_is_validated_property(self):
        self.assertEqual(self.main_string1.is_validated, False)
        self.assertEqual(self.translated_string1.is_validated, True)
        self.assertEqual(self.translated_string2.is_validated, False)

    def test_is_main_string_property(self):
        self.assertEqual(self.main_string1.is_main_string, True)
        self.assertEqual(self.translated_string1.is_main_string, False)

    def test_manager_strings(self):
        expected_result = [self.translated_string1, self.translated_string2]
        self.assertEquals(list(models.TranslatedString.objects.strings(self.translation)), expected_result)

    def test_manager_keys(self):
        expected_result = [self.main_string1, self.main_string2]
        self.assertEquals(list(models.TranslatedString.objects.keys(self.translation)), expected_result)

    def test_manager_validated(self):
        expected_result = [self.translated_string1]
        self.assertEquals(list(models.TranslatedString.objects.validated(self.translation)), expected_result)

    def test_manager_not_validated(self):
        expected_result = [self.translated_string2]
        self.assertEquals(list(models.TranslatedString.objects.not_validated(self.translation)), expected_result)
