from django.contrib.auth import get_user_model
from django.db import models

from clarity_project.core.mixins import BaseModel

User = get_user_model()


class SchoolApplication(BaseModel):
    is_family_business_owner = models.BooleanField(default=False)
    is_family_returning = models.BooleanField(default=False)
    did_family_file_us_taxes = models.BooleanField(default=False)
    submitter = models.ForeignKey(User, on_delete=models.CASCADE)
