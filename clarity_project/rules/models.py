from django.db import models

from clarity_project.core.mixins import BaseModel
from clarity_project.rules.enums import ActionChoices
from clarity_project.rules.enums import ConditionChoices
from clarity_project.rules.enums import ConditionConjunctionChoices
from clarity_project.rules.enums import TriggerChoices


class Trigger(BaseModel):
    trigger_type = models.CharField(choices=TriggerChoices.choices, max_length=50)


class Condition(BaseModel):
    condition_type = models.CharField(choices=ConditionChoices.choices, max_length=50)
    conjunction = models.CharField(choices=ConditionConjunctionChoices.choices, max_length=50)


class Action(BaseModel):
    action_type = models.CharField(choices=ActionChoices.choices, max_length=50)


class Rule(BaseModel):
    triggers = models.ManyToManyField(Trigger)
    conditions = models.ManyToManyField(Condition)
    actions = models.ManyToManyField(Action)
