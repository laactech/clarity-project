import logging

from clarity_project.applications.models import SchoolApplication
from clarity_project.rules.enums import ConditionConjunctionChoices
from clarity_project.rules.enums import ConditionTypeChoices
from clarity_project.rules.models import Rule

logger = logging.getLogger(__name__)


def evaluate_rule_conditions(rule: Rule, school_application: SchoolApplication) -> bool:
    result = None
    for rule_condition in rule.rule_conditions.all():
        condition = rule_condition.condition
        conjunction = rule_condition.conjunction
        condition_evaluation = CONDITION_TYPE_MAPPING[condition.condition_type](school_application)
        logger.info(
            "Evaluating condition", extra={"condition_id": condition.id, "condition_type": condition.condition_type}
        )
        print(condition_evaluation)
        if result is None:
            result = condition_evaluation
        elif conjunction == ConditionConjunctionChoices.AND:
            result = result and condition_evaluation
        elif conjunction == ConditionConjunctionChoices.OR:
            result = result or condition_evaluation
        else:
            raise NotImplementedError(conjunction)

        logger.info(
            "Evaluated condition",
            extra={"condition_id": condition.id, "result": result, "condition_type": condition.condition_type},
        )

    return result


def _is_business_owner(school_application: SchoolApplication) -> bool:
    return school_application.is_family_business_owner


def _is_family_returning(school_application: SchoolApplication) -> bool:
    return school_application.is_family_returning


def _did_family_file_us_taxes(school_application: SchoolApplication) -> bool:
    return school_application.did_family_file_us_taxes


CONDITION_TYPE_MAPPING = {
    ConditionTypeChoices.IS_RETURNING: _is_family_returning,
    ConditionTypeChoices.IS_BUSINESS_OWNER: _is_business_owner,
    ConditionTypeChoices.FILED_US_TAXES: _did_family_file_us_taxes,
}
