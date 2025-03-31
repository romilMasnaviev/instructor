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
    group_id = models.AutoField(primary_key=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=255)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.group_name} ({self.status})"


# 4. TrainingGroupParachutist (Обучающийся в группе)
class TrainingGroupParachutist(models.Model):
    parachutist = models.ForeignKey(Parachutist, on_delete=models.CASCADE)
    group = models.ForeignKey(TrainingGroup, on_delete=models.CASCADE)
    theory_passed = models.BooleanField(default=False)
    practice_passed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('parachutist', 'group')

    def __str__(self):
        return f"{self.parachutist} in {self.group}"


# 5. JumpGroup (Прыжковая группа)
class JumpGroup(models.Model):
    instructor_air = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='air_instructor')
    instructor_ground = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='ground_instructor')
    jump_date = models.DateTimeField()
    aircraft_type = models.CharField(max_length=255)
    altitude = models.PositiveIntegerField(help_text="Высота в метрах")
    status = models.CharField(max_length=50, choices=[('Planned', 'Запланирован'), ('Completed', 'Завершен'), ('Cancelled', 'Отменен')], default='Planned')

    def __str__(self):
        return f"Прыжковая группа {self.jump_date} ({self.status})"


# 6. JumpRequest (Заявка на прыжок)
class JumpRequest(models.Model):
    parachutist = models.ForeignKey(Parachutist, on_delete=models.CASCADE)
    jump_group = models.ForeignKey(JumpGroup, on_delete=models.CASCADE)
    request_status = models.CharField(max_length=50, choices=[('Pending', 'Ожидает'), ('Approved', 'Одобрена'), ('Denied', 'Отклонена')], default='Pending')

    def __str__(self):
        return f"Заявка на прыжок {self.parachutist} в {self.jump_group} ({self.request_status})"


# 7. JumpAssignment (Задание на прыжок)
class JumpAssignment(models.Model):
    parachutist = models.ForeignKey(Parachutist, on_delete=models.CASCADE)
    jump_group = models.ForeignKey(JumpGroup, on_delete=models.CASCADE)
    task = models.TextField()

    def __str__(self):
        return f"Задание для {self.parachutist} в {self.jump_group}"


# 8. PreJumpCheck (Проверка перед прыжком)
class PreJumpCheck(models.Model):
    pre_jump_check_id = models.AutoField(primary_key=True)
    jump_group = models.ForeignKey(JumpGroup, on_delete=models.CASCADE)
    theory_passed = models.BooleanField(default=False)
    practice_passed = models.BooleanField(default=False)
    medical_certified = models.BooleanField(default=False)
    equipment_checked = models.BooleanField(default=False)

    def __str__(self):
        return f"Проверка перед прыжком для {self.jump_group} ({'Пройдено' if self.theory_passed else 'Не пройдено'})"

