from django.db import models
from django.contrib.auth.models import AbstractUser

class Account(AbstractUser):
    account_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)  # Автоматически хэшируется Django
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=255)  # Поле для полного имени

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']  # Добавляем full_name как обязательное поле для миграции

    class Meta:
        db_table = 'account'

    def __str__(self):
        return self.email

    # Можно добавить метод для возврата полного имени
    def get_full_name(self):
        return self.full_name
