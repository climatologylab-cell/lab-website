from django.contrib import admin
from django import forms
from datetime import datetime
from import_export import resources, fields, widgets
from import_export.widgets import DateWidget
from .models import Publication, Journal, Conference, Book, Guideline, OtherDocument
from core.admin_base import BaseAdmin

class FlexibleDateWidget(DateWidget):
    """
    Widget to handle multiple date formats.
    """
    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return None
        
        # Try different formats
        formats = [
            '%Y-%m-%d',      # 2024-01-01
            '%b %d, %Y',     # Jan 1, 2024
            '%d-%m-%Y',      # 01-01-2024
            '%d/%m/%Y',      # 01/01/2024
            '%m/%d/%Y',      # 01/01/2024 (US)
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(str(value).strip(), fmt).date()
            except (ValueError, TypeError):
                continue
                
        # If all fail, try the default behavior (which might raise validation error)
        return super().clean(value, row, *args, **kwargs)

class PublicationResource(resources.ModelResource):
    citation = fields.Field(attribute='citation', column_name='DATA')
    publication_date = fields.Field(
        attribute='publication_date', 
        column_name='Date', 
        widget=FlexibleDateWidget()
    )
    external_link = fields.Field(attribute='external_link', column_name='LINK')
    
    def before_import_row(self, row, **kwargs):
        # Ensure required fields are populated
        if 'title' not in row or not row['title']:
            # Use specific parts of citation or just the whole citation as title fallback
            data = row.get('DATA', '')
            row['title'] = data[:499] if data else 'Untitled Publication'
            
        if 'authors' not in row or not row['authors']:
            row['authors'] = "Unknown Authors"

    class Meta:
        model = Publication
        fields = ('id', 'citation', 'publication_date', 'external_link', 'title', 'authors', 'journal', 'category', 'cover_image')
        export_order = fields

@admin.register(Publication)
class PublicationAdmin(BaseAdmin):
    resource_class = PublicationResource
    list_display = ['title', 'journal', 'publication_date', 'category', 'scope', 'is_featured', 'is_active']
    list_filter = ['category', 'scope', 'is_featured', 'is_active', 'publication_date']
    search_fields = ['title', 'authors', 'journal', 'doi', 'abstract']
    date_hierarchy = 'publication_date'
    ordering = ['-publication_date']
    
    fieldsets = (
        ('Publication Information', {
            'fields': ('title', 'authors', 'category', 'scope', 'citation', 'abstract')
        }),
        ('Publication Details', {
            'fields': ('journal', 'publication_date', 'volume', 'issue', 'pages', 'doi')
        }),
        ('Files & Links', {
            'fields': ('cover_image', 'pdf_file', 'external_link', 'related_projects')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_active')
        }),
    )

class BaseProxyAdmin(PublicationAdmin):
    """Base admin for proxy models to hide category field and filter queryset"""
    def get_queryset(self, request):
        return super().get_queryset(request).filter(category=self.category_value)

    def save_model(self, request, obj, form, change):
        obj.category = self.category_value
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Hide category field since it's implied
        if 'category' in form.base_fields:
            form.base_fields['category'].widget = forms.HiddenInput()
            form.base_fields['category'].initial = self.category_value
        return form

@admin.register(Journal)
class JournalAdmin(BaseProxyAdmin):
    category_value = 'journal'

@admin.register(Conference)
class ConferenceAdmin(BaseProxyAdmin):
    category_value = 'conference'

@admin.register(Book)
class BookAdmin(BaseProxyAdmin):
    category_value = 'book'

@admin.register(Guideline)
class GuidelineAdmin(BaseProxyAdmin):
    category_value = 'guideline'

@admin.register(OtherDocument)
class OtherDocumentAdmin(BaseProxyAdmin):
    category_value = 'other'
