import logging

from celery import shared_task

from clarity_project.rules.action_runner import run_action
from clarity_project.rules.condition_evaluator import evaluate_rule_conditions
from clarity_project.rules.models import RuleRun

logger = logging.getLogger(__name__)


@shared_task(autoretry_for=(RuleRun.DoesNotExist,), max_retries=2, retry_backoff=True)
def execute_rule_run(rule_run_id: str):
    rule_run = RuleRun.objects.get(id=rule_run_id)
    rule = rule_run.rule
    logger.info("Executing rule run", extra={"rule_run_id": rule_run_id})

    condition_result = evaluate_rule_conditions(rule, rule_run.school_application)
    logger.info(
        "Condition for rule evaluated", extra={"condition_result": condition_result, "rule_run_id": rule_run_id}
    )

    if condition_result:
        logger.info("Running actions due to condition result evaluation", extra={"rule_run_id": rule_run_id})
        for action in rule.actions.all():
            run_action(action, rule_run.school_application)
