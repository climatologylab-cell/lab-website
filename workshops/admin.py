from django.contrib import admin
from .models import Workshop
from core.admin_base import BaseAdmin

@admin.register(Workshop)
class WorkshopAdmin(BaseAdmin):
    list_display = ['title', 'event_date', 'posted_date', 'is_active']
    list_filter = ['is_active', 'event_date']
    search_fields = ['title', 'description']
    date_hierarchy = 'event_date'
    ordering = ['-event_date']
    
    fieldsets = (
        ('Workshop Information', {
            'fields': ('title', 'description', 'event_date', 'link')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
