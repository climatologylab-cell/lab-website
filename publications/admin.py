import re
from django.contrib import admin
from django import forms
from datetime import datetime
from import_export import resources, fields, widgets
from import_export.widgets import DateWidget
from .models import Publication, Journal, Conference, Book, Guideline, OtherDocument
from core.admin_base import BaseAdmin

from .resources import (
    PublicationResource, JournalResource, BookResource, 
    ConferenceResource, ThesisResource, GuidelineResource
)

@admin.register(Publication)
class PublicationAdmin(BaseAdmin):
    resource_class = PublicationResource
    list_display = ['title', 'journal', 'publication_date', 'category', 'scope', 'is_featured', 'is_active']
    list_filter = ['category', 'scope', 'is_featured', 'is_active', 'publication_date']
    search_fields = ['title', 'authors', 'journal', 'doi', 'abstract']
    actions = ['fix_misplaced_categories']

    @admin.action(description="Fix categories based on 'journal' field name")
    def fix_misplaced_categories(self, request, queryset):
        # Emergency fix for "Unknown Authors" and misplaced book chapters
        count = 0
        for obj in queryset:
            if 'chapter' in obj.citation.lower() or 'book' in obj.citation.lower():
                obj.category = 'book'
                obj.save()
                count += 1
        self.message_user(request, f"Updated {count} publications to Book Chapters.")

class BaseProxyAdmin(PublicationAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(category=self.category_value)
    def save_model(self, request, obj, form, change):
        obj.category = self.category_value
        super().save_model(request, obj, form, change)

@admin.register(Journal)
class JournalAdmin(BaseProxyAdmin):
    category_value = 'journal'
    resource_class = JournalResource

@admin.register(Conference)
class ConferenceAdmin(BaseProxyAdmin):
    category_value = 'conference'
    resource_class = ConferenceResource

@admin.register(Book)
class BookAdmin(BaseProxyAdmin):
    category_value = 'book'
    resource_class = BookResource

@admin.register(Guideline)
class GuidelineAdmin(BaseProxyAdmin):
    category_value = 'guideline'
    resource_class = GuidelineResource

@admin.register(OtherDocument)
class OtherDocumentAdmin(BaseProxyAdmin):
    category_value = 'other'
