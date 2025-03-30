import sys

from django.apps import AppConfig
from django.core.management import call_command


class InstructorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'instructors'
    def ready(self):
        if 'runserver' in sys.argv:  # Проверяем, что запускается сервер
            call_command('flush', '--no-input')
            call_command('migrate')