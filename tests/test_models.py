#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-rockpile
------------

Tests for `django-rockpile` modules module.
"""

from django.test import TestCase
from rockpile import models


class BasicProjectMixin(object):

    def setUp(self):
        pass
        # TODO: Create here needed objects
        # models.TranslationProject.objects.create()


class TestTranslatedString(BasicProjectMixin, TestCase):
    pass

    # TODO: make a lot of tests!
