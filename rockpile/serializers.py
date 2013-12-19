'''
REST serializers for rockpile
=================================

'''

from rest_framework import serializers
from .models import Translator, Owner, TranslationProject, TranslatedString, Translation


class TranslatorSerializer(serializers.ModelSerializer):
    """
    Translator serializer
    """

    class Meta:
        model = Translator
        fields = ('user',)
        read_only_fields = ('user',)


class OwnerSerializer(serializers.ModelSerializer):
    """
    Owner serializer
    """

    class Meta:
        model = Owner
        fields = ('user',)


class TranslationProjectSerializer(serializers.ModelSerializer):
    """
    TranslationProject serializer
    """

    class Meta:
        model = TranslationProject
        fields = ('owner', 'name')


class TranslatedStringSerializer(serializers.ModelSerializer):
    """
    TranslatedString serializer
    """

    class Meta:
        model = TranslatedString
        fields = ('key', 'value', 'translation', 'validated_by')


class TranslationSerializer(serializers.ModelSerializer):
    """
    Translation serializer
    """

    class Meta:
        model = Translation
        fields = ('language', 'translators', 'project')
