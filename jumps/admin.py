from django.contrib import admin
from .models import *

@admin.register(JumpGroup)
class JumpGroupAdmin(admin.ModelAdmin):
    list_display = ('jump_date', 'location', 'altitude', 'status', 'instructor')
    search_fields = ('location',)
    list_filter = ('status', 'jump_date', 'instructor')

@admin.register(JumpRequest)
class JumpRequestAdmin(admin.ModelAdmin):
    list_display = ('parachutist', 'jump_group', 'request_status', 'result_status', 'requested_at')
    search_fields = ('parachutist__first_name', 'jump_group__location')
    list_filter = ('request_status', 'result_status', 'jump_group')
