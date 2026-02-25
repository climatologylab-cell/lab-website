from django.contrib import admin
from .models import (
    SiteSettings, HomePageStats, HomePageContent, RTNotice, 
    Tutorial, CarouselImage, ImpactStory, 
    ResearchHighlight, PolicyImpact
)
from .admin_base import BaseAdmin

@admin.register(SiteSettings)
class SiteSettingsAdmin(BaseAdmin):
    list_display = ['site_name', 'email', 'phone']
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'site_description', 'phone', 'email', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'linkedin_url')
        }),
    )


@admin.register(HomePageStats)
class HomePageStatsAdmin(BaseAdmin):
    list_display = ['publications_count', 'projects_count', 'outreach_programs_count', 'updated_at']

@admin.register(ImpactStory)
class ImpactStoryAdmin(BaseAdmin):
    list_display = ['title', 'category', 'impact_metrics', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['title', 'description', 'category']

@admin.register(ResearchHighlight)
class ResearchHighlightAdmin(BaseAdmin):
    list_display = ['title', 'icon', 'order', 'is_active']
    list_filter = ['icon', 'is_active']
    search_fields = ['title', 'description']

@admin.register(PolicyImpact)
class PolicyImpactAdmin(BaseAdmin):
    list_display = ['year', 'title', 'organization', 'is_active']
    list_filter = ['year', 'is_active']
    search_fields = ['title', 'description', 'organization']
    
    def has_add_permission(self, request):
        # Only allow one instance
        return HomePageStats.objects.count() == 0


@admin.register(HomePageContent)
class HomePageContentAdmin(BaseAdmin):
    list_display = ['welcome_title', 'professor_name', 'is_active']
    list_filter = ['is_active']


@admin.register(RTNotice)
class RTNoticeAdmin(BaseAdmin):
    list_display = ['notice_type', 'title', 'event_date', 'is_active']
    list_filter = ['notice_type', 'is_active', 'event_date']
    search_fields = ['title', 'description']


@admin.register(CarouselImage)
class CarouselImageAdmin(BaseAdmin):
    list_display = ['title', 'image_preview', 'order', 'is_active', 'created_at']
    list_filter = ['is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'alt_text']
    readonly_fields = ['image_preview', 'created_at']

    def image_preview(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; border-radius: 4px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"



# Import-Export Resource for Tutorial
from import_export import resources, fields

class TutorialResource(resources.ModelResource):
    """Resource class for importing/exporting Tutorial data"""
    
    # Map CSV headers to model fields
    # CSV headers: "Title:", "External link:"
    # Model fields: title, external_link
    title = fields.Field(
        column_name='Title:',  # CSV header with colon
        attribute='title'       # Model field
    )
    
    external_link = fields.Field(
        column_name='External link:',  # CSV header with colon and space
        attribute='external_link'       # Model field
    )
    
    class Meta:
        model = Tutorial
        fields = ('title', 'external_link', 'is_active', 'order')
        import_id_fields = []  # Don't use any field as unique identifier (create new each time)
        skip_unchanged = False
        report_skipped = False
    
    def before_save_instance(self, instance, row, **kwargs):
        """Auto-extract YouTube thumbnail before saving"""
        # Set defaults
        if not hasattr(instance, 'is_active') or instance.is_active is None:
            instance.is_active = True
        if not hasattr(instance, 'order') or instance.order is None:
            instance.order = 0
        
        # Auto-extract thumbnail URL from YouTube link
        if instance.external_link and not instance.thumbnail_url:
            youtube_id = instance.get_youtube_id()
            if youtube_id:
                instance.thumbnail_url = f"https://img.youtube.com/vi/{youtube_id}/hqdefault.jpg"


@admin.register(Tutorial)
class TutorialAdmin(BaseAdmin):
    resource_class = TutorialResource  # Use custom Resource class for import/export
    
    list_display = ['title', 'is_playlist', 'playlist_id', 'lecture_number', 'thumbnail_preview', 'is_active', 'order', 'created_date']
    list_filter = ['is_active', 'is_playlist', 'playlist_id', 'created_date']
    search_fields = ['title', 'playlist_id']
    list_editable = ['is_active', 'order', 'is_playlist', 'lecture_number']
    readonly_fields = ['thumbnail_preview', 'created_date', 'updated_date']
    
    fieldsets = (
        ('Tutorial Information', {
            'fields': ('title', 'external_link')
        }),
        ('Playlist Settings', {
            'fields': ('playlist_id', 'is_playlist', 'lecture_number'),
            'description': 'Set playlist_id to group videos. Mark first video as is_playlist=True, others as False with lecture numbers.'
        }),
        ('Display Order', {
            'fields': ('order',)
        }),
        ('Thumbnail', {
            'fields': ('thumbnail_url', 'thumbnail_preview'),
            'description': 'YouTube thumbnails are auto-extracted. You can override with a custom URL.'
        }),
        ('Status & Dates', {
            'fields': ('is_active', 'created_date', 'updated_date')
        }),
    )
    
    def thumbnail_preview(self, obj):
        """Display thumbnail preview in admin"""
        from django.utils.html import format_html
        thumbnail = obj.get_thumbnail()
        if thumbnail:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-width: 200px; max-height: 112px; border-radius: 8px;" /></a>',
                obj.external_link,
                thumbnail
            )
        return "No thumbnail"
    thumbnail_preview.short_description = "Thumbnail Preview"

