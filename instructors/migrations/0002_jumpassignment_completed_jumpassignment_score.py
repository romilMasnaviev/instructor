# Generated by Django 4.2.20 on 2025-03-31 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jumpassignment',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='jumpassignment',
            name='score',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True),
        ),
    ]
