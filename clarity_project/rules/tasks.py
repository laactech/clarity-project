from celery import shared_task

from clarity_project.rules.models import RuleRun


@shared_task()
def execute_rule_run(rule_run_id: str):
    rule_run = RuleRun.objects.get(id=rule_run_id)
    rule = rule_run.rule
