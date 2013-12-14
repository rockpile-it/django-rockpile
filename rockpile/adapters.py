'''
Adapters for rockpile
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

from collections import MutableMapping, OrderedDict
from lxml import etree


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

        super(AndroidStrings, self).__init__()

        # LXML parses the XML and stores data in a python dict for an easier use
        self._xml = etree.parse(file_obj)

        # Stores data in order
        self._data = OrderedDict()
        for element in self._xml.findall("./string"):
            self._data[element.attrib['name']] = element.text
