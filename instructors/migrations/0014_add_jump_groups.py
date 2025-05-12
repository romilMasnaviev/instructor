import datetime
from django.utils import timezone
from django.db import migrations


def create_jump_groups(apps, schema_editor):
    Instructor = apps.get_model('instructors', 'Instructor')
    Parachutist = apps.get_model('instructors', 'Parachutist')
    JumpGroup = apps.get_model('instructors', 'JumpGroup')
    JumpGroupParachutist = apps.get_model('instructors', 'JumpGroupParachutist')

    # Получаем инструкторов
    instructor1 = Instructor.objects.get(pk=1)
    instructor2 = Instructor.objects.get(pk=2)
    instructor4 = Instructor.objects.get(pk=4)
    instructor5 = Instructor.objects.get(pk=5)

    # Получаем парашютистов
    p1 = Parachutist.objects.get(pk=1)
    p2 = Parachutist.objects.get(pk=2)
    p3 = Parachutist.objects.get(pk=3)
    p4 = Parachutist.objects.get(pk=4)
    p5 = Parachutist.objects.get(pk=5)

    now = timezone.now()

    # Создаем первую прыжковую группу
    jump_group1 = JumpGroup.objects.create(
        instructor_air=instructor1,
        instructor_ground=instructor2,
        group_name='Прыжковая группа 1',
        jump_date=now + datetime.timedelta(days=1),
        aircraft_type='Ан-2',
        altitude=4000,
        status='created'
    )

    # Добавляем парашютистов 3 и 4 в первую группу
    JumpGroupParachutist.objects.create(parachutist=p3, jump_group=jump_group1)
    JumpGroupParachutist.objects.create(parachutist=p4, jump_group=jump_group1)

    # Создаем вторую прыжковую группу
    jump_group2 = JumpGroup.objects.create(
        instructor_air=instructor4,
        instructor_ground=instructor5,
        group_name='Прыжковая группа 2',
        jump_date=now + datetime.timedelta(days=2),
        aircraft_type='Л-410',
        altitude=3000,
        status='created'
    )

    # Добавляем парашютистов 1, 2 и 5 во вторую группу
    JumpGroupParachutist.objects.create(parachutist=p1, jump_group=jump_group2)
    JumpGroupParachutist.objects.create(parachutist=p2, jump_group=jump_group2)
    JumpGroupParachutist.objects.create(parachutist=p5, jump_group=jump_group2)


class Migration(migrations.Migration):
    dependencies = [
        ('instructors', '0013_add_training_group_parachutists'),
    ]

    operations = [
        migrations.RunPython(create_jump_groups),
    ]
