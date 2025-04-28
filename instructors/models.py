from django.db import models


# 1. Parachutist (Парашютист)

class Parachutist(models.Model):
    parachutist_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# 2. Instructor (Инструктор)
class Instructor(models.Model):
    instructor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    qualification = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.qualification})"


# 3. TrainingGroup (Учебная группа)
class TrainingGroup(models.Model):
    # Определяем возможные статусы для учебной группы через choices
    STATUS_CHOICES = [
        ('created', 'Создана'),  # Статус "Создана"
        ('in_progress', 'В процессе'),  # Статус "В процессе"
        ('completed', 'Завершена'),  # Статус "Завершена"
    ]

    group_id = models.AutoField(primary_key=True)
    instructor = models.ForeignKey('Instructor',
                                   on_delete=models.CASCADE)  # Убедитесь, что модель Instructor определена
    group_name = models.CharField(max_length=255)  # Название группы
    start_date_time = models.DateTimeField()  # Дата и время начала
    end_date_time = models.DateTimeField(null=True, blank=True)  # Дата и время завершения
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')  # Статус с choices

    def __str__(self):
        return f"{self.group_name} ({self.get_status_display()})"  # Текстовое представление статуса через get_status_display()


# 4. TrainingGroupParachutist (Обучающийся в группе)
class TrainingGroupParachutist(models.Model):
    parachutist = models.ForeignKey(Parachutist, on_delete=models.CASCADE)
    group = models.ForeignKey(TrainingGroup, on_delete=models.CASCADE)
    theory_passed = models.BooleanField(default=False)
    practice_passed = models.BooleanField(default=False)
    exam_passed = models.BooleanField(default=False)  # Новое поле для зачета
    ready_for_jump = models.BooleanField(default=False)  # Новое поле

    def __str__(self):
        return f"{self.parachutist} in {self.group}"

    def save(self, *args, **kwargs):
        # Обновляем поле ready_for_jump на основе значений чекпоинтов
        self.ready_for_jump = self.theory_passed and self.practice_passed and self.exam_passed
        super().save(*args, **kwargs)


# 5. JumpGroup (Прыжковая группа)
class JumpGroup(models.Model):
    instructor_air = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='air_instructor')
    instructor_ground = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='ground_instructor')
    group_name = models.CharField(max_length=255, default="")  # <--- новое поле: название группы
    start_date_time = models.DateTimeField(null=True, blank=True)  # <--- новое поле: начало
    end_date_time = models.DateTimeField(null=True, blank=True)  # <--- новое поле: завершение
    jump_date = models.DateTimeField()
    aircraft_type = models.CharField(max_length=255)
    altitude = models.PositiveIntegerField(help_text="Высота в метрах")
    status = models.CharField(
        max_length=50,
        choices=[
            ('Created', 'Создана'),
            ('Pre-Flight Preparation', 'Предполетная подготовка'),
            ('Jump In Progress', 'Прыжок в процессе'),
            ('Completed', 'Завершена'),
            ('Cancelled', 'Отменена')
        ],
        default='Created'
    )

    def __str__(self):
        return f"Прыжковая группа {self.group_name} ({self.status})"


# 6. JumpRequest (Заявка на прыжок)
class JumpRequest(models.Model):
    parachutist = models.ForeignKey(Parachutist, on_delete=models.CASCADE)
    jump_group = models.ForeignKey(JumpGroup, on_delete=models.CASCADE)
    request_status = models.CharField(max_length=50, choices=[('Pending', 'Ожидает'), ('Approved', 'Одобрена'),
                                                              ('Denied', 'Отклонена')], default='Pending')

    def __str__(self):
        return f"Заявка на прыжок {self.parachutist} в {self.jump_group} ({self.request_status})"


class JumpAssignment(models.Model):
    parachutist = models.ForeignKey(Parachutist, on_delete=models.CASCADE)
    jump_group = models.ForeignKey(JumpGroup, on_delete=models.CASCADE)
    task = models.TextField()
    score = models.PositiveSmallIntegerField(null=True, blank=True,
                                             choices=[(i, str(i)) for i in range(6)])  # Оценка от 0 до 5
    completed = models.BooleanField(default=False)  # Фиксация выполнения прыжка

    def __str__(self):
        return f"Задание для {self.parachutist} в {self.jump_group}"


# 8. PreJumpCheck (Проверка перед прыжком)
class PreJumpCheck(models.Model):
    pre_jump_check_id = models.AutoField(primary_key=True)
    jump_group = models.ForeignKey(JumpGroup, on_delete=models.CASCADE)
    parachutist = models.ForeignKey('Parachutist', on_delete=models.CASCADE)  # Добавляем связь с моделью Parachutist
    theory_passed = models.BooleanField(default=False)
    practice_passed = models.BooleanField(default=False)
    medical_certified = models.BooleanField(default=False)
    equipment_checked = models.BooleanField(default=False)
    correct_assignment = models.BooleanField(default=False)

    def __str__(self):
        return f"Проверка перед прыжком для {self.jump_group} парашютиста {self.parachutist} ({'Пройдено' if self.theory_passed else 'Не пройдено'})"
