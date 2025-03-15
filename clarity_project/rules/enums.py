from django.db import models


class TriggerChoices(models.TextChoices):
    APPLICATION_SUBMISSION = "application_submission", "Application Submission"

class ConditionChoices(models.TextChoices):
    IS_BUSINESS_OWNER = "is_business_owner", "Is Business Owner"
    IS_RETURNING = "is_returning", "Is Returning"
    FILED_US_TAXES = "filed_us_taxes", "Filed US Taxes"

class ConditionConjunctionChoices(models.TextChoices):
    AND = "and", "And"
    OR = "or", "Or"

class ActionChoices(models.TextChoices):
    DOCUMENT_REQUESTED = "document_requested", "Document Requested"


class DocumentType(models.TextChoices):
    W2 = "W2", "W2"
    PAY_STUB = "pay_stub", "Pay Stub"
    BUSINESS_TAX_DOCUMENT = "business_tax_document", "Business Tax Document"
    BANK_STATEMENT = "bank_statement", "Bank Statement"
