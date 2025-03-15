import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(
        _("Datetime Created"),
        auto_now_add=True,
        editable=False,
    )
    history = HistoricalRecords(inherit=True)
    archived = models.BooleanField(_("Archived"), default=False)

    class Meta:
        abstract = True
