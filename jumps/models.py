from django.db import models
from instructors.models import Instructor
from parachutists.models import Parachutist

class JumpGroup(models.Model):
    STATUS_CHOICES = [
        ('Planned', 'Запланирован'),
        ('Completed', 'Завершен'),
        ('Cancelled', 'Отменен'),
    ]

    jump_group_id = models.AutoField(primary_key=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, db_column='instructor_id')
    jump_date = models.DateField()
    location = models.CharField(max_length=255)
    altitude = models.PositiveIntegerField(help_text="Высота в метрах")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Planned')

    class Meta:
        db_table = 'jump_group'
        ordering = ['-jump_date']

    def __str__(self):
        return f"Прыжок {self.jump_date} ({self.status})"

class JumpRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Ожидает'),
        ('Approved', 'Одобрена'),
        ('Denied', 'Отклонена'),
    ]
    RESULT_CHOICES = [
        ('Success', 'Успешно'),
        ('Failed', 'Неудачно'),
        ('Cancelled', 'Отменен'),
    ]

    request_id = models.AutoField(primary_key=True)
    parachutist = models.ForeignKey(Parachutist, on_delete=models.CASCADE, db_column='parachutist_id')
    jump_group = models.ForeignKey(JumpGroup, on_delete=models.CASCADE, db_column='jump_group_id')
    request_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    result_status = models.CharField(max_length=50, choices=RESULT_CHOICES, blank=True, null=True)
    jump_result = models.CharField(max_length=255, blank=True, null=True)
    requested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'jump_request'
        ordering = ['-requested_at']

    def __str__(self):
        return f"{self.parachutist} -> {self.jump_group} ({self.request_status})"