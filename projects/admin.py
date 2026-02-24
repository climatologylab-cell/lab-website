from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import ResearchProject
from .resources import ResearchProjectResource
from core.admin_base import BaseAdmin

@admin.register(ResearchProject)
class ResearchProjectAdmin(BaseAdmin):
    resource_class = ResearchProjectResource
    
    # List display - only fields that exist in model
    list_display = [
        'title', 
        'project_type', 
        'status',
        'role', 
        'funding_agency',
        'start_date', 
        'is_active',
        'image'
    ]
    
    # List filters - only fields that exist
    list_filter = [
        'project_type', 
        'status', 
        'role',
        'is_active'
    ]
    
    # Search fields - only fields that exist
    search_fields = [
        'title', 
        'description', 
        'collaborators', 
        'funding_agency',
        'partner_institutions'
    ]
    
    date_hierarchy = 'start_date'
    ordering = ['-start_date']
    
    fieldsets = (
        ('Project Classification', {
            'fields': ('project_type', 'is_active')
        }),
        ('Core Information', {
            'fields': ('title', 'description', 'status', 'image', 'external_link')
        }),
        ('Funding & Finance', {
            'fields': ('funding_agency', 'grant_amount')
        }),
        ('Team & Collaborators', {
            'fields': ('role', 'collaborators', 'partner_institutions')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date')
        }),
    )
