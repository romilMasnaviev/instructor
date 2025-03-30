from django.contrib import admin
from .models import *

# Для TrainingGroup
@admin.register(TrainingGroup)
class TrainingGroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'instructor', 'status', 'start_date', 'end_date')
    search_fields = ('group_name',)
    list_filter = ('status', 'start_date', 'instructor')

# Для TrainingGroupParachutist
@admin.register(TrainingGroupParachutist)
class TrainingGroupParachutistAdmin(admin.ModelAdmin):
    list_display = ('group', 'parachutist', 'theory_passed', 'practice_passed', 'certificate_check')
    search_fields = ('group__group_name', 'parachutist__first_name')
    list_filter = ('theory_passed', 'practice_passed', 'certificate_check', 'group')
