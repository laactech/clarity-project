from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from clarity_project.applications.api.serializers import SchoolApplicationSerializer
from clarity_project.applications.models import SchoolApplication
from clarity_project.rules.enums import TriggerTypeChoices
from clarity_project.rules.models import Rule
from clarity_project.rules.models import RuleRun
from clarity_project.rules.tasks import execute_rule_run


class SchoolApplicationViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = SchoolApplication.objects.all()
    serializer_class = SchoolApplicationSerializer

    def perform_create(self, serializer):
        serializer.save(submitter=self.request.user)
        school_application_id = serializer.data["id"]

        application_submission_rules = Rule.objects.filter(
            trigger__trigger_type=TriggerTypeChoices.APPLICATION_SUBMISSION, enabled=True
        )
        for rule in application_submission_rules:
            rule_run = RuleRun.objects.create(rule=rule, school_application_id=school_application_id)
            execute_rule_run.delay(rule_run.id)
