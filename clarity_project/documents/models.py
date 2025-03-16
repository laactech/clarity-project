from django.db import models

from clarity_project.core.mixins import BaseModel
from clarity_project.documents.enums import DocumentStatus
from clarity_project.documents.enums import DocumentType


class Document(BaseModel):
    file = models.FileField(upload_to="documents/%Y/%m/%d", null=True, blank=True)
    document_type = models.CharField(choices=DocumentType.choices, max_length=50)
    last_email_notification_sent_at = models.DateTimeField(null=True, blank=True)

    @property
    def status(self):
        if not self.file:
            return DocumentStatus.REQUESTED
        return DocumentStatus.UPLOADED
