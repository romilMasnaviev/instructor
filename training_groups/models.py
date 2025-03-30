from django.db import models
from instructors.models import Instructor
from parachutists.models import Parachutist

class TrainingGroup(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Активна'),
        ('Completed', 'Завершена'),
        ('Archived', 'В архиве'),
    ]

    group_id = models.AutoField(primary_key=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, db_column='instructor_id')
    group_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Active')

    class Meta:
        db_table = 'training_group'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.group_name} ({self.status})"

class TrainingGroupParachutist(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(TrainingGroup, on_delete=models.CASCADE, db_column='group_id')
    parachutist = models.ForeignKey(Parachutist, on_delete=models.CASCADE, db_column='parachutist_id')
    theory_passed = models.BooleanField(default=False)
    practice_passed = models.BooleanField(default=False)
    certificate_check = models.BooleanField(default=False)

    class Meta:
        db_table = 'training_group_parachutist'
        unique_together = ('group', 'parachutist')

    def __str__(self):
        return f"{self.parachutist} in {self.group}"