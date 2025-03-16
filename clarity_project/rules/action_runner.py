import logging

from django.core.mail import send_mail
from django.utils import timezone

from clarity_project.applications.models import SchoolApplication
from clarity_project.documents.models import Document
from clarity_project.rules.enums import ActionTypeChoices
from clarity_project.rules.models import Action

logger = logging.getLogger(__name__)


def run_action(action: Action, school_application: SchoolApplication):
    logger.info("Running action", extra={"action": action.id, "action_type": action.action_type})
    ACTION_TYPE_MAPPING[action.action_type](action, school_application)


def _run_document_requested_action(action: Action, school_application: SchoolApplication):
    send_mail(
        "Document Requested",
        f"Hi, please submit these documents: {action.requested_document_types}",
        "noreply@myawesomeapp.com",
        [school_application.submitter.email],
        fail_silently=False,
    )
    logger.info("Sent email", extra={"action": action.id, "action_type": action.action_type,"email": school_application.submitter.email})

    for doc_type in action.requested_document_types:
        Document.objects.create(document_type=doc_type, last_email_notification_sent_at=timezone.now())
    logger.info("Created documents", extra={"action": action.id, "action_type": action.action_type,
                                            "requested_document_types": action.requested_document_types})


ACTION_TYPE_MAPPING = {
    ActionTypeChoices.DOCUMENT_REQUESTED: _run_document_requested_action,
}
