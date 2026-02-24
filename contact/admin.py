from django.contrib import admin
from .models import ContactSubmission
from core.admin_base import BaseAdmin

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(BaseAdmin):
    list_display = ['name', 'email', 'phone', 'submitted_date', 'is_read']
    list_filter = ['is_read', 'submitted_date']
    search_fields = ['name', 'email', 'query']
    date_hierarchy = 'submitted_date'
    ordering = ['-submitted_date']
    readonly_fields = ['submitted_date']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Query', {
            'fields': ('query', 'submitted_date')
        }),
        ('Admin', {
            'fields': ('is_read', 'admin_notes')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Auto-mark as read when admin views
        return qs
    
    def has_delete_permission(self, request, obj=None):
        # Allow deletion of old submissions
        return True
