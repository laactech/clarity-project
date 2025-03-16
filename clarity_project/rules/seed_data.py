from sqlite3 import IntegrityError

from clarity_project.rules.enums import TriggerTypeChoices, ActionTypeChoices, ConditionTypeChoices
from clarity_project.rules.models import Trigger, Action, Condition


def seed_data():
    for trigger_type in TriggerTypeChoices:
        try:
            Trigger.objects.create(trigger_type=trigger_type)
        except IntegrityError:
            pass

    for action_type in ActionTypeChoices:
        try:
            Action.objects.create(action_type=action_type)
        except IntegrityError:
            pass

    for condition_type in ConditionTypeChoices:
        try:
            Condition.objects.create(condition_type=condition_type)
        except IntegrityError:
            pass
