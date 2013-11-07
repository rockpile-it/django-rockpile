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
        self.owner = models.Owner(user=self.user)
        self.translator = models.Translator(user=self.user)
        self.translation_project = models.TranslationProject.objects.create(name='Test project')


class TestTranslatedString(BasicProjectMixin, TestCase):
    pass

    # TODO: make a lot of tests!
