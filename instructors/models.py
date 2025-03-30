from django.db import models
from accounts.models import Account

class Instructor(models.Model):
    QUALIFICATION_CHOICES = [
        ('AFF', 'AFF-инструктор'),
        ('Tandem', 'Тандем-инструктор'),
        ('PDP', 'ПДП-инструктор'),
    ]
    STATUS_CHOICES = [
        ('Active', 'Активен'),
        ('Inactive', 'Неактивен'),
        ('Vacation', 'В отпуске'),
    ]

    instructor_id = models.AutoField(primary_key=True)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, db_column='account_id')
    qualification = models.CharField(max_length=50, choices=QUALIFICATION_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Active')

    class Meta:
        db_table = 'instructor'

    def __str__(self):
        return f"{self.account.get_full_name()} ({self.qualification})"