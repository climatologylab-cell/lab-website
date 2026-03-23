import re
from django.contrib import admin
from django import forms
from datetime import datetime
from import_export import resources, fields, widgets
from import_export.widgets import DateWidget
from .models import Publication, Journal, Conference, Book, Guideline, OtherDocument
from core.admin_base import BaseAdmin

class FlexibleDateWidget(DateWidget):
    """Widget to handle multiple date formats and extraction from text."""
    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            # Try to extract year from citation if date is missing
            citation = row.get('DATA', '')
            year_match = re.search(r'\((\d{4})\)', citation)
            if year_match:
                return datetime(int(year_match.group(1)), 1, 1).date()
            return None
        
        # Try common formats
        formats = ['%Y-%m-%d', '%b %d, %Y', '%d-%m-%Y', '%d/%m/%Y', '%m/%d/%Y']
        for fmt in formats:
            try:
                return datetime.strptime(str(value).strip(), fmt).date()
            except (ValueError, TypeError):
                continue
        return super().clean(value, row, *args, **kwargs)

class PublicationResource(resources.ModelResource):
    # Map CSV columns (case-insensitive mapping handled in before_import_row)
    citation = fields.Field(attribute='citation', column_name='DATA')
    publication_date = fields.Field(attribute='publication_date', column_name='DATE', widget=FlexibleDateWidget())
    external_link = fields.Field(attribute='external_link', column_name='LINK')
    title = fields.Field(attribute='title', column_name='TITLE')
    authors = fields.Field(attribute='authors', column_name='AUTHORS')
    
    def before_import_row(self, row, **kwargs):
        # 1. Handle case-insensitive headers (DATE vs Date vs date)
        for key in list(row.keys()):
            if key.upper() == 'AUTHORS' and key != 'AUTHORS': row['AUTHORS'] = row.pop(key)
            if key.upper() == 'TITLE' and key != 'TITLE': row['TITLE'] = row.pop(key)
            if key.upper() == 'DATE' and key != 'DATE': row['DATE'] = row.pop(key)

        # 2. Extract Title and Authors from Citation (DATA) if missing
        citation = row.get('DATA', '')
        if citation:
            # Attempt to split "Title. Authors (Year). Journal."
            # Common pattern: parts[0] is title, parts[1] is authors
            parts = [p.strip() for p in citation.split('.') if p.strip()]
            
            if not row.get('TITLE') or row.get('TITLE') == row.get('DATA'):
                if parts: row['TITLE'] = parts[0][:499]
                
            if not row.get('AUTHORS') or row.get('AUTHORS') == "Unknown Authors":
                # Look for the segment containing the year (2024)
                for part in parts:
                    if re.search(r'\(\d{4}\)', part):
                        # The segment before the year usually contains authors
                        author_part = part.split('(')[0].strip()
                        if author_part:
                            row['AUTHORS'] = author_part
                            break
                # Fallback: if second part exists, assume it's authors
                if (not row.get('AUTHORS') or row.get('AUTHORS') == "Unknown Authors") and len(parts) > 1:
                    row['AUTHORS'] = parts[1]

    class Meta:
        model = Publication
        fields = ('id', 'citation', 'publication_date', 'external_link', 'title', 'authors', 'journal', 'category')
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
