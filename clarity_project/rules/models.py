from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import CheckConstraint
from django.db.models import UniqueConstraint

from clarity_project.applications.models import SchoolApplication
from clarity_project.core.mixins import BaseModel
from clarity_project.documents.enums import DocumentType
from clarity_project.rules.enums import ActionTypeChoices
from clarity_project.rules.enums import ConditionConjunctionChoices
from clarity_project.rules.enums import ConditionTypeChoices
from clarity_project.rules.enums import TriggerTypeChoices


class Trigger(BaseModel):
    trigger_type = models.CharField(choices=TriggerTypeChoices.choices, max_length=50)

    class Meta:
        constraints = [UniqueConstraint(fields=["trigger_type"], name="trigger_type_unique")]


class Condition(BaseModel):
    condition_type = models.CharField(choices=ConditionTypeChoices.choices, max_length=50)

    class Meta:
        constraints = [UniqueConstraint(fields=["condition_type"], name="condition_type_unique")]


class Action(BaseModel):
    action_type = models.CharField(choices=ActionTypeChoices.choices, max_length=50)
    requested_document_types = ArrayField(
        models.CharField(choices=DocumentType.choices, max_length=50), null=True, blank=True
    )

    class Meta:
        constraints = [
            CheckConstraint(
                check=models.Q(
                    action_type=ActionTypeChoices.DOCUMENT_REQUESTED, requested_document_types__isnull=False
                )
                | ~models.Q(action_type=ActionTypeChoices.DOCUMENT_REQUESTED),
                name="requested_document_types_required_for_document_requested",
            )
        ]


class Rule(BaseModel):
    trigger = models.ForeignKey(Trigger, on_delete=models.PROTECT, related_name="rules")
    conditions = models.ManyToManyField(Condition, related_name="rules", through="RuleCondition")
    actions = models.ManyToManyField(Action, related_name="rules")
    enabled = models.BooleanField(default=True)


class RuleCondition(BaseModel):
    condition = models.ForeignKey(Condition, on_delete=models.PROTECT, related_name="rule_conditions")
    rule = models.ForeignKey(Rule, on_delete=models.PROTECT, related_name="rule_conditions")
    conjunction = models.CharField(choices=ConditionConjunctionChoices.choices, max_length=50)


class RuleRun(BaseModel):
    rule = models.ForeignKey(Rule, on_delete=models.PROTECT, related_name="rule_runs")
    school_application = models.ForeignKey(SchoolApplication, on_delete=models.PROTECT, related_name="rule_runs")
    completed = models.BooleanField(default=False)
