# Generated by Django 4.2.20 on 2025-04-28 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructors', '0005_traininggroupparachutist_ready_for_jump'),
    ]

    operations = [
        migrations.AddField(
            model_name='jumpgroup',
            name='end_date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jumpgroup',
            name='group_name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='jumpgroup',
            name='start_date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='jumpgroup',
            name='status',
            field=models.CharField(choices=[('Created', 'Создана'), ('Progress', 'В процессе'), ('Jump', 'Выполнение прыжка'), ('Completed', 'Завершен'), ('Cancelled', 'Отменен')], default='Created', max_length=50),
        ),
    ]
