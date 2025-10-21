# village_app/management/commands/test_command.py
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'A test command to verify management commands are working'

    def handle(self, *args, **options):
        self.stdout.write("Test command is working!")