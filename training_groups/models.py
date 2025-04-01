from django.db import models
from parachutists.models import Parachutist

class TrainingGroup(models.Model):
    STATUS_CHOICES = [
        ('open', 'Открыта'),
        ('in_progress', 'В процессе'),
        ('closed', 'Закрыта'),
    ]

    name = models.CharField(max_length=255)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    parachutists = models.ManyToManyField(Parachutist, related_name="training_groups", blank=True)

    def __str__(self):
        return self.name

