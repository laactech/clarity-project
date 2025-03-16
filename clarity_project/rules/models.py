from django.db import models

from clarity_project.applications.models import SchoolApplication
from clarity_project.core.mixins import BaseModel
from clarity_project.rules.enums import ActionTypeChoices
from clarity_project.rules.enums import ConditionConjunctionChoices
from clarity_project.rules.enums import ConditionTypeChoices
from clarity_project.rules.enums import TriggerTypeChoices


class Trigger(BaseModel):
    trigger_type = models.CharField(choices=TriggerTypeChoices.choices, max_length=50)


class Condition(BaseModel):
    condition_type = models.CharField(choices=ConditionTypeChoices.choices, max_length=50)
    conjunction = models.CharField(choices=ConditionConjunctionChoices.choices, max_length=50)


class Action(BaseModel):
    action_type = models.CharField(choices=ActionTypeChoices.choices, max_length=50)


class Rule(BaseModel):
    trigger = models.ForeignKey(Trigger, on_delete=models.PROTECT, related_name="rules")
    conditions = models.ManyToManyField(Condition, related_name="rules")
    actions = models.ManyToManyField(Action, related_name="rules")
    enabled = models.BooleanField(default=True)


class RuleRun(BaseModel):
    rule = models.ForeignKey(Rule, on_delete=models.PROTECT, related_name="rule_runs")
    school_application = models.ForeignKey(SchoolApplication, on_delete=models.PROTECT, related_name="rule_runs")
    completed = models.BooleanField(default=False)
