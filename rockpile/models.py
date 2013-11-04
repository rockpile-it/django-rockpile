'''
Translation models for rockpile
=================================


Support for multiple translation systems
-----------------------------------------

Gettext
++++++++++++++

`gettext` is one of the most common i18n systems used by Django (.po files)

There is a library called `polib` supporting from python 2.4 to python 3.X (*rosetta* is using it)


Android
++++++++++++++

Android uses a more naive approach, a bunch of xmls splitted in folders:

::
    res/values-es/strings.xml
    res/values-en/strings.xml
    res/values/strings.xml


Each `strings.xml` file represents one language.

'''

from collections import MutableMapping
from lxml import etree
from django.db import models
from django.conf.global_settings import LANGUAGES
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


# Translated list of languages (#TODO: I'm not completeley sure if this works...)
TRANSLATED_LANGUAGES = [(lang_code, _(lang_name)) for lang_code, lang_name in LANGUAGES]


class TranslatableStrings(MutableMapping):
    """
    Base class that uses self._data as internal dict storage
    """

    def __init__(self):
        """
        Constructor
        """

        self._data = {}

    def __len__(self):
        """
        Returns the number of translatable strings
        """

        return len(self._data)

    def __getitem__(self, key):
        """
        Returns the current value for the translation key

        :param key: Translation key
        :type key: str
        """

        return self._data[key]

    def __setitem__(self, key, value):
        """
        Assigns a value to the given translation key

        :param key: Translation key
        :type key: str
        :param key: Translation value
        :type key: str
        """

        self._data[key] = value

    def __delitem__(self, key):
        """
        Deletes a translation key
        """

        del self._data[key]

    def __iter__(self):
        """
        Iterator
        """

        return iter(self._data)


class AndroidStrings(TranslatableStrings):
    """
    Helper class to support strings.xml files that Android uses for internationalization

    Usage:

    >>> android_strings = AndoridStrings(my_fd)
    >>> len(android_strings)
    69
    >>> android_strings['app_name']
    'My app name'
    >>> android_strings['app_name'] = 'Changed name'
    >>> android_strings['app_name']
    'Changed name'
    """

    def __init__(self, file_obj):
        """
        Constructor

        :param file_obj: File-like object containing XML
        :type file_obj: file-like obj
        """

        # LXML parses the XML and stores data in a python dict for an easier use
        self._xml = etree.parse(file_obj)
        self._data = {e.attrib['name']: e.text for e in self._xml.findall("./string")}


class Translator(models.Model):
    """
    Represents the translator role
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    # TODO: Add more interesting fields here (gamify this!)


class Owner(models.Model):
    """
    Represents the owner role
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL)


class TranslationProject(models.Model):
    """
    TranslationProject is a helper model that contains multiple translations and is
    the highest abstraction level to the translation system.
    """

    owner = models.ForeignKey(Owner)


class Translation(models.Model):
    """
    Translation model represents the translation for one language and this is linked
    to multiple translators
    """

    language = models.CharField(max_length=7, choices=TRANSLATED_LANGUAGES)
    translators = models.ManyToManyField(Translator)
    project = models.ForeignKey(TranslationProject)


class TranslatedString(models.Model):
    """
    Represents the lowest level of the translation, a single string.

    A string is linked to a translation and also has a reference to another string that
    will act as the "key" of the translated string.
    """

    key = models.ForeignKey("self", verbose_name=_("Traduction key"), db_index=True, null=True)
    value = models.TextField(_("Traduction value"))
    translation = models.ForeignKey(Translation)
