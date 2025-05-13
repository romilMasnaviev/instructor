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
    medical_certified = models.BooleanField('Мед. сертификация', default=False)
    """
    Наличие необходимых для прыжка мед. бумаг.
    """
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
    group_name = models.CharField(max_length=255, default="")
    start_date_time = models.DateTimeField(null=True, blank=True)
    end_date_time = models.DateTimeField(null=True, blank=True)
    jump_date = models.DateTimeField()
    aircraft_type = models.CharField(max_length=255)
    altitude = models.PositiveIntegerField(help_text="Высота в метрах")
    status = models.CharField(
        max_length=50,
        choices=[
            ('created', 'Создана'),
            ('Pre-Flight Preparation', 'Предполетная подготовка'),
            ('Jump In Progress', 'Прыжок в процессе'),
            ('Completed', 'Завершена'),
            ('Cancelled', 'Отменена')
        ],
        default='Created'
    )

    def __str__(self):
        return f"Прыжковая группа {self.group_name} ({self.status})"


# 6. Задание на прыжок
class JumpAssignment(models.Model):
    parachutist = models.ForeignKey(Parachutist, on_delete=models.CASCADE)
    jump_group = models.ForeignKey(JumpGroup, on_delete=models.CASCADE)
    task = models.TextField()
    score = models.PositiveSmallIntegerField(null=True, blank=True,
                                             choices=[(i, str(i)) for i in range(6)])  # Оценка от 0 до 5
    completed = models.BooleanField(default=False)  # Фиксация выполнения прыжка

    def __str__(self):
        return f"Задание для {self.parachutist} в {self.jump_group}"


# 7. парашютист в прыжковой группе
class JumpGroupParachutist(models.Model):
    parachutist = models.ForeignKey(Parachutist, on_delete=models.CASCADE)
    jump_group = models.ForeignKey(JumpGroup, on_delete=models.CASCADE)
    request_status = models.CharField('Статус заявки', max_length=50, choices=[('Pending', 'Ожидает'), ('Approved', 'Одобрена'),
                                                              ('Denied', 'Отклонена')], default='Pending')
    medical_checkup_passed = models.BooleanField('Медицинское освидетельствование', default=False)
    """
    Проверка состояния здоровья на месте.
    """
    equipment_checked = models.BooleanField('Снаряжение проверено', default=False)
    correct_assignment = models.BooleanField('Корректное задание', default=False)

    def __str__(self):
        return f"Заявка на прыжок {self.parachutist} в {self.jump_group} ({self.request_status})"
