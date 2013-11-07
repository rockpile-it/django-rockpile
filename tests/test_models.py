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

        # Translated strings
        self.main_string = models.TranslatedString.objects.create(value='Hello world', translation=self.translation)
        models.TranslatedString.objects.create(key=self.main_string, value='Hola mundo', translation=self.translation, validated_by=self.translator)
        self.main_string2 = models.TranslatedString.objects.create(value='Testing string', translation=self.translation)
        models.TranslatedString.objects.create(key=self.main_string2, value='Probando cadena', translation=self.translation)


class TestTranslation(BasicProjectMixin, TestCase):

    def test_percentage_completion(self):
        self.assertEqual(self.translation.percentage_completed, 50.0)
