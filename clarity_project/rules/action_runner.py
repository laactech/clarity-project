import logging

from clarity_project.applications.models import SchoolApplication
from clarity_project.rules.enums import ActionTypeChoices
from clarity_project.rules.models import Action
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

def run_action(action: Action, school_application: SchoolApplication):
    logger.debug("Running action", extra={"action": action.id, "action_type": action.action_type})
    ACTION_TYPE_MAPPING[action.action_type](school_application)


def _run_document_requested_action(school_application: SchoolApplication):
    # TODO: how to get document type
    send_mail(
        "Document Requested",
        "Hi, please submit this document.",
        "noreply@myawesomeapp.com",
        [school_application.submitter.email],
        fail_silently=False,
    )


ACTION_TYPE_MAPPING = {
    ActionTypeChoices.DOCUMENT_REQUESTED: _run_document_requested_action,
}
