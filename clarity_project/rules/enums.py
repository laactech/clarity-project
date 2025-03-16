from django.db import models


class TriggerTypeChoices(models.TextChoices):
    APPLICATION_SUBMISSION = "application_submission", "Application Submission"


class ConditionTypeChoices(models.TextChoices):
    IS_BUSINESS_OWNER = "is_business_owner", "Is Business Owner"
    IS_RETURNING = "is_returning", "Is Returning"
    FILED_US_TAXES = "filed_us_taxes", "Filed US Taxes"


class ConditionConjunctionChoices(models.TextChoices):
    AND = "and", "And"
    OR = "or", "Or"


class ActionTypeChoices(models.TextChoices):
    DOCUMENT_REQUESTED = "document_requested", "Document Requested"
