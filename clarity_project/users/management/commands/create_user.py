import getpass
import sys

from django.core.management.base import BaseCommand
from django.db import transaction

from clarity_project.users.services import create_new_user


class Command(BaseCommand):
    def handle(self, *args, **options):
        choice = input(
            "WARNING: This command creates a super user with access to the django admin"
            " panel. Are you sure you want to do that? Enter yes to continue: "
        )  # nosec
        if choice.lower() != "yes":
            sys.exit()
        email = input("Enter the email to use for your user: ")  # nosec
        name = input("Enter your name: ")  # nosec
        password = getpass.getpass("Enter your desired password: ")  # nosec
        with transaction.atomic():
            user, _ = create_new_user(
                email,
                password=password,
                is_superuser=True,
                user_full_name=name,
            )
