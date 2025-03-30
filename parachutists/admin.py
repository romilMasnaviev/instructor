from django.contrib import admin
from .models import *

# Для Parachutist
@admin.register(Parachutist)
class ParachutistAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'account', 'contact_info')
    search_fields = ('first_name', 'last_name', 'account__email')
    list_filter = ('account',)

# Для ParachutistStatusHistory
@admin.register(ParachutistStatusHistory)
class ParachutistStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('parachutist', 'status', 'changed_at')
    search_fields = ('parachutist__first_name', 'parachutist__last_name')
    list_filter = ('status',)