from django.db import migrations


def add_instructors(apps, schema_editor):
    Instructor = apps.get_model('your_app', 'Instructor')

    # Создание тестовых данных
    instructors = [
        Instructor(
            first_name="Иван",
            middle_name="Александрович",
            last_name="Петров",
            contact_info="ivan.petrov@example.com",
            qualification="Мастер спорта",
            status="Активен"
        ),
        Instructor(
            first_name="Мария",
            middle_name="Викторовна",
            last_name="Сидорова",
            contact_info="maria.sidorova@example.com",
            qualification="Инструктор первой категории",
            status="Активен"
        ),
        Instructor(
            first_name="Дмитрий",
            middle_name="Сергеевич",
            last_name="Козлов",
            contact_info="dmitry.kozlova@example.com",
            qualification="Кандидат в мастера спорта",
            status="На обучении"
        ),
        Instructor(
            first_name="Елена",
            middle_name="Ивановна",
            last_name="Горшкова",
            contact_info="elena.gorshkova@example.com",
            qualification="Инструктор высшей категории",
            status="Активен"
        ),
        Instructor(
            first_name="Алексей",
            middle_name="Петрович",
            last_name="Михайлов",
            contact_info="aleksey.mikhailov@example.com",
            qualification="Мастер спорта международного класса",
            status="Активен"
        ),
    ]

    # Сохранение данных в базе
    for instructor in instructors:
        instructor.save()


def remove_instructors(apps, schema_editor):
    Instructor = apps.get_model('', 'Instructor')
    Instructor.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('your_app', '0001_initial'),  # Замените на имя предыдущей миграции
    ]

    operations = [
        migrations.RunPython(add_instructors, remove_instructors),
    ]