# instructors/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_migrate


class InstructorsConfig(AppConfig):
    name = 'instructors'

    def ready(self):
        # Подключаем сигнал для создания начальных данных после миграций
        from .signals import create_initial_data
        post_migrate.connect(create_initial_data, sender=self)
