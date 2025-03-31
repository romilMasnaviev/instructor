# instructors/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Instructor, Parachutist

@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    if not Instructor.objects.exists():
        Instructor.objects.create(
            first_name="John", middle_name="Doe", last_name="Smith", contact_info="john.doe@example.com",
            qualification="Advanced Instructor", status="Active"
        )
        Instructor.objects.create(
            first_name="Jane", middle_name="Doe", last_name="Brown", contact_info="jane.brown@example.com",
            qualification="Intermediate Instructor", status="Active"
        )
        Instructor.objects.create(
            first_name="Alice", middle_name="Ann", last_name="Johnson", contact_info="alice.johnson@example.com",
            qualification="Beginner Instructor", status="Inactive"
        )

    if not Parachutist.objects.exists():
        Parachutist.objects.create(
            first_name="Michael", middle_name="A.", last_name="Williams", contact_info="michael.williams@example.com"
        )
        Parachutist.objects.create(
            first_name="Emily", middle_name="B.", last_name="Davis", contact_info="emily.davis@example.com"
        )
        Parachutist.objects.create(
            first_name="David", middle_name="C.", last_name="Miller", contact_info="david.miller@example.com"
        )
