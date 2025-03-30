from django.contrib import admin
from .models import *

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('account', 'qualification', 'status')
    search_fields = ('account__email', 'qualification')
    list_filter = ('status',)