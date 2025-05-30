# Generated by Django 4.2.20 on 2025-05-12

from django.db import migrations


def create_training_group_parachutists(apps, schema_editor):
    Parachutist = apps.get_model('instructors', 'Parachutist')
    TrainingGroup = apps.get_model('instructors', 'TrainingGroup')
    TrainingGroupParachutist = apps.get_model('instructors', 'TrainingGroupParachutist')

    # Создаем объекты TrainingGroupParachutist с парашютистами в группах
    group1 = TrainingGroup.objects.get(group_id=1)  # Группа 1
    group2 = TrainingGroup.objects.get(group_id=2)  # Группа 2

    parachutist1 = Parachutist.objects.get(parachutist_id=1)
    parachutist2 = Parachutist.objects.get(parachutist_id=2)
    parachutist3 = Parachutist.objects.get(parachutist_id=3)
    parachutist4 = Parachutist.objects.get(parachutist_id=4)
    parachutist5 = Parachutist.objects.get(parachutist_id=5)

    # Создаем записи для TrainingGroupParachutist с умолчаниями (False)
    TrainingGroupParachutist.objects.create(
        parachutist=parachutist1, group=group1, theory_passed=False, practice_passed=False, exam_passed=False,
        ready_for_jump=False
    )
    TrainingGroupParachutist.objects.create(
        parachutist=parachutist2, group=group1, theory_passed=False, practice_passed=False, exam_passed=False,
        ready_for_jump=False
    )
    TrainingGroupParachutist.objects.create(
        parachutist=parachutist3, group=group2, theory_passed=False, practice_passed=False, exam_passed=False,
        ready_for_jump=False
    )
    TrainingGroupParachutist.objects.create(
        parachutist=parachutist4, group=group2, theory_passed=False, practice_passed=False, exam_passed=False,
        ready_for_jump=False
    )
    TrainingGroupParachutist.objects.create(
        parachutist=parachutist5, group=group2, theory_passed=False, practice_passed=False, exam_passed=False,
        ready_for_jump=False
    )


class Migration(migrations.Migration):
    dependencies = [
        ('instructors', '0012_add_training_groups'),
    ]

    operations = [
        migrations.RunPython(create_training_group_parachutists),
    ]
