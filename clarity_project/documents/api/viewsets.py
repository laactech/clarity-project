from rest_framework import viewsets

from clarity_project.documents.api.serializers import DocumentSerializer
from clarity_project.documents.models import Document


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
