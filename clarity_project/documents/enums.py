from django.db import models


class DocumentType(models.TextChoices):
    W2 = "W2", "W2"
    PAY_STUB = "pay_stub", "Pay Stub"
    BUSINESS_TAX_DOCUMENT = "business_tax_document", "Business Tax Document"
    BANK_STATEMENT = "bank_statement", "Bank Statement"


class DocumentStatus(models.TextChoices):
    REQUESTED = "requested", "Requested"
    UPLOADED = "uploaded", "Uploaded"
