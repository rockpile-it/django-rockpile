#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-rockpile
------------

Tests for `django-rockpile` REST API.
"""

from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from django.test import TestCase
from django.test.client import Client


class TestTranslatorViewset(TestCase):
    """
    """

    def setUp(self):
        self.user = get_user_model()(username='john')
        self.user.set_password('top_secret')
        self.user.save()
        self.client = Client()
        self.client.login(username='john', password='top_secret')

    def test_list(self):
        response = self.client.get(reverse('translator-list'), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, '[]')

    def test_create(self):
        response = self.client.post(reverse('translator-list'), follow=True)
        self.assertEquals(response.status_code, 201)
