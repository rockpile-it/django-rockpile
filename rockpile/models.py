'''
Translation models for rockpile
=================================

'''

from django.db import models
from django.conf.global_settings import LANGUAGES
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


# Translated list of languages (#TODO: I'm not completeley sure if this works...)
TRANSLATED_LANGUAGES = [(lang_code, _(lang_name)) for lang_code, lang_name in LANGUAGES]


class Translator(models.Model):
    """
    Represents the translator role
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL)


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
    name = models.CharField(_('Project name'), max_length=255)


class TranslatedStringManager(models.Manager):

    def strings(self, translation):
        """
        Returns a queryset with translated strings
        """

        return self.get_queryset().filter(translation=translation, key__isnull=False)

    def keys(self, translation):
        """
        Returns a queryset with "main" strings
        """

        return self.get_queryset().filter(translation=translation, key__isnull=True)

    def validated(self, translation):
        """
        Returns a queryset with validated strings
        """

        return self.get_queryset().filter(translation=translation).exclude(validated_by__isnull=True)

    def not_validated(self, translation):
        """
        Returns a queryset with not validated strings
        """

        return self.get_queryset().filter(translation=translation, validated_by__isnull=True)


class TranslatedString(models.Model):
    """
    Represents the lowest level of the translation, a single string.

    A string is linked to a translation and also has a reference to another string that
    will act as the "key" of the translated string.

    A string may be validated by a translator.
    """

    key = models.ForeignKey("self", verbose_name=_("Translation key"), db_index=True, null=True)
    value = models.TextField(_("Translation value"))
    translation = models.ForeignKey("Translation", verbose_name=_("Translation"))
    validated_by = models.ForeignKey(Translator, verbose_name=_("Validated by"), null=True)
    objects = TranslatedStringManager()

    class Meta:
        order_with_respect_to = 'translation'

    @property
    def is_validated(self):
        """
        Shortcut method to check if a string has been validated
        """
        return bool(self.validated_by)

    @property
    def is_main_string(self):
        """
        Shortcut method to check if a string is the original string to translate
        """
        return self.key is None


class Translation(models.Model):
    """
    Translation model represents the translation for one language and this is linked
    to multiple translators
    """

    language = models.CharField(_("Language"), max_length=7, choices=TRANSLATED_LANGUAGES)
    translators = models.ManyToManyField(Translator, verbose_name=_("Translators"))
    project = models.ForeignKey(TranslationProject, verbose_name=_("Project"))

    @property
    def percentage_completed(self):
        """
        Returns the percentage of completion for this translation
        """

        num_strings = TranslatedString.objects.strings(self).count()
        if num_strings:
            num_validated_strings = TranslatedString.objects.validated(self).count()
            return num_validated_strings * 100.0 / num_strings
        else:
            return 0.0
