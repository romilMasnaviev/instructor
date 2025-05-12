from django.db import migrations


def create_jump_assignments(apps, schema_editor):
    Parachutist = apps.get_model('instructors', 'Parachutist')
    JumpGroup = apps.get_model('instructors', 'JumpGroup')
    JumpAssignment = apps.get_model('instructors', 'JumpAssignment')

    parachutist3 = Parachutist.objects.get(pk=3)
    parachutist4 = Parachutist.objects.get(pk=4)
    parachutist5 = Parachutist.objects.get(pk=5)

    group1 = JumpGroup.objects.get(pk=1)
    group2 = JumpGroup.objects.get(pk=2)

    JumpAssignment.objects.create(
        parachutist=parachutist3,
        jump_group=group1,
        task="Совершить прыжок с высоты 1200 м с выполнением контрольных движений.",
    )

    JumpAssignment.objects.create(
        parachutist=parachutist4,
        jump_group=group1,
        task="Прыжок с высоты 1200 м, проверка навыков стабилизации.",
    )

    JumpAssignment.objects.create(
        parachutist=parachutist5,
        jump_group=group2,
        task="Контрольный прыжок с высоты 1000 м. Уделить внимание положению тела в воздухе.",
    )


class Migration(migrations.Migration):
    dependencies = [
        ('instructors', '0014_add_jump_groups'),
    ]

    operations = [
        migrations.RunPython(create_jump_assignments),
    ]
