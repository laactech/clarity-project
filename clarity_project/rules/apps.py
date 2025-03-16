from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RulesConfig(AppConfig):
    name = "clarity_project.rules"
    verbose_name = _("Rules")
