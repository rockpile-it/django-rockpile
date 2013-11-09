#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test adapters
--------------

Tests for `django-rockpile` adapters module.
"""
import tempfile

from django.test import TestCase

from rockpile.adapters import AndroidStrings


class AndroidStringsTest(TestCase):

    def setUp(self):
        input_data = u'''<?xml version="1.0" encoding="utf-8"?>
                         <resources>
                            <string name="app_name">Hola rockpile</string>
                            <string name="info_text">probando android</string>
                         <color name="White">#ffffff</color>
                         </resources>'''
        file_obj = tempfile.TemporaryFile()
        file_obj.write(input_data.encode('utf-8'))
        file_obj.seek(0)
        self.android_strings = AndroidStrings(file_obj)
        file_obj.close()

    def test_len(self):
        self.assertEqual(len(self.android_strings), 2)

    def test_read(self):
        self.assertEqual(self.android_strings['app_name'], 'Hola rockpile')

    def test_write(self):
        self.android_strings['app_name'] = 'Hello rockpile'
        self.assertEqual(self.android_strings['app_name'], 'Hello rockpile')

    def test_delete(self):
        del self.android_strings['app_name']
        self.assertNotIn('app_name', self.android_strings)

    def test_iter(self):
        expected_value = [('app_name', 'Hola rockpile'), ('info_text', 'probando android')]
        self.assertEqual(expected_value, list(self.android_strings.items()))
