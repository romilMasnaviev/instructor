# Generated by Django 4.2.20 on 2025-03-30 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('instructor_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('middle_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('contact_info', models.CharField(max_length=255)),
                ('qualification', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='JumpGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jump_date', models.DateTimeField()),
                ('aircraft_type', models.CharField(max_length=255)),
                ('altitude', models.PositiveIntegerField(help_text='Высота в метрах')),
                ('status', models.CharField(choices=[('Planned', 'Запланирован'), ('Completed', 'Завершен'), ('Cancelled', 'Отменен')], default='Planned', max_length=50)),
                ('instructor_air', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='air_instructor', to='instructors.instructor')),
                ('instructor_ground', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ground_instructor', to='instructors.instructor')),
            ],
        ),
        migrations.CreateModel(
            name='Parachutist',
            fields=[
                ('parachutist_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('middle_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('contact_info', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TrainingGroup',
            fields=[
                ('group_id', models.AutoField(primary_key=True, serialize=False)),
                ('group_name', models.CharField(max_length=255)),
                ('start_date_time', models.DateTimeField()),
                ('end_date_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(max_length=50)),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructors.instructor')),
            ],
        ),
        migrations.CreateModel(
            name='PreJumpCheck',
            fields=[
                ('pre_jump_check_id', models.AutoField(primary_key=True, serialize=False)),
                ('theory_passed', models.BooleanField(default=False)),
                ('practice_passed', models.BooleanField(default=False)),
                ('medical_certified', models.BooleanField(default=False)),
                ('equipment_checked', models.BooleanField(default=False)),
                ('jump_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructors.jumpgroup')),
            ],
        ),
        migrations.CreateModel(
            name='JumpRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_status', models.CharField(choices=[('Pending', 'Ожидает'), ('Approved', 'Одобрена'), ('Denied', 'Отклонена')], default='Pending', max_length=50)),
                ('jump_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructors.jumpgroup')),
                ('parachutist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructors.parachutist')),
            ],
        ),
        migrations.CreateModel(
            name='JumpAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.TextField()),
                ('jump_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructors.jumpgroup')),
                ('parachutist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructors.parachutist')),
            ],
        ),
        migrations.CreateModel(
            name='TrainingGroupParachutist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theory_passed', models.BooleanField(default=False)),
                ('practice_passed', models.BooleanField(default=False)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructors.traininggroup')),
                ('parachutist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructors.parachutist')),
            ],
            options={
                'unique_together': {('parachutist', 'group')},
            },
        ),
    ]
