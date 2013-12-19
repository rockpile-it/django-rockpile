from rest_framework import viewsets, permissions
from .models import Translator
from .serializers import TranslatorSerializer


class TranslatorViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Translator.objects.all()
    serializer_class = TranslatorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def pre_save(self, obj):
        obj.user = self.request.user
