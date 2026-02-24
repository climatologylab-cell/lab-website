from django.db import models

class SiteSettings(models.Model):
    """Global site settings"""
    site_name = models.CharField(max_length=200, default="Climatology Lab")
    site_description = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return self.site_name


class HomePageStats(models.Model):
    """Homepage statistics"""
    publications_count = models.IntegerField(default=100)
    projects_count = models.IntegerField(default=120)
    outreach_programs_count = models.IntegerField(default=50)
    years_of_research = models.IntegerField(default=15)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Homepage Statistics"
        verbose_name_plural = "Homepage Statistics"
    
    def __str__(self):
        return f"Stats - {self.updated_at.strftime('%Y-%m-%d')}"


class HomePageContent(models.Model):
    """Homepage welcome content"""
    welcome_title = models.CharField(max_length=500)
    welcome_text = models.TextField()
    professor_name = models.CharField(max_length=200, default="Professor Mahua Mukherjee")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Homepage Content"
        verbose_name_plural = "Homepage Content"
    
    def __str__(self):
        return self.welcome_title


class ResearchNotice(models.Model):
    """Research notices/workshops"""
    title = models.CharField(max_length=300)
    description = models.TextField()
    event_date = models.DateField()
    posted_date = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Research Notice"
        verbose_name_plural = "Research Notices"
        ordering = ['-event_date']
    
    def __str__(self):
        return f"{self.title} - {self.event_date}"


class TechnologyNotice(models.Model):
    """Technology notices/workshops"""
    title = models.CharField(max_length=300)
    description = models.TextField()
    event_date = models.DateField()
    posted_date = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Technology Notice"
        verbose_name_plural = "Technology Notices"
        ordering = ['-event_date']
    
    def __str__(self):
        return f"{self.title} - {self.event_date}"


class Tutorial(models.Model):
    """Tutorials with external links (YouTube, websites)"""
    title = models.CharField(max_length=300)
    external_link = models.URLField(help_text="YouTube link or external website URL")
    thumbnail_url = models.URLField(blank=True, help_text="Auto-extracted for YouTube, or manual URL")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order (lower numbers first)")
    
    # Playlist fields
    playlist_id = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="ID to group videos into a playlist (e.g., 'urban-ecosystem')"
    )
    is_playlist = models.BooleanField(
        default=False,
        help_text="True if this is the main playlist video, False if it's a lecture"
    )
    lecture_number = models.IntegerField(
        blank=True, 
        null=True,
        help_text="Order of lecture within playlist (1, 2, 3...)"
    )
    
    class Meta:
        verbose_name = "Tutorial"
        verbose_name_plural = "Tutorials"
        ordering = ['order', '-created_date']
    
    def __str__(self):
        return self.title

    def get_youtube_id(self):
        """Extract YouTube video ID from URL"""
        import re
        if 'youtube.com' in self.external_link or 'youtu.be' in self.external_link:
            # Handle different YouTube URL formats
            patterns = [
                r'(?:youtube\.com\/watch\?v=)([^&]+)',
                r'(?:youtu\.be\/)([^?]+)',
                r'(?:youtube\.com\/embed\/)([^?]+)',
            ]
            for pattern in patterns:
                match = re.search(pattern, self.external_link)
                if match:
                    return match.group(1)
        return None
    
    def get_thumbnail(self):
        """Get thumbnail URL (YouTube auto or manual)"""
        if self.thumbnail_url:
            return self.thumbnail_url
        
        # Auto-extract YouTube thumbnail
        youtube_id = self.get_youtube_id()
        if youtube_id:
            # Use hqdefault (480x360) - more reliable than maxresdefault
            return f"https://img.youtube.com/vi/{youtube_id}/hqdefault.jpg"
        
        # Default placeholder if no thumbnail
        return None
    
    def save(self, *args, **kwargs):
        """Auto-populate thumbnail for YouTube links"""
        if not self.thumbnail_url:
            youtube_id = self.get_youtube_id()
            if youtube_id:
                self.thumbnail_url = f"https://img.youtube.com/vi/{youtube_id}/maxresdefault.jpg"
        super().save(*args, **kwargs)


class CarouselImage(models.Model):
    """Images for the home page hero carousel"""
    title = models.CharField(max_length=200, help_text="Internal title for the image")
    image = models.ImageField(upload_to='carousel/', help_text="Image file (recommended 600x400 or similar aspect ratio)")
    alt_text = models.CharField(max_length=200, blank=True, help_text="Alt text for accessibility")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers first)")
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide from the carousel")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Carousel Image"
        verbose_name_plural = "Carousel Images"
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title

class ImpactStory(models.Model):
    """Success stories for the Impact page"""
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100, help_text="e.g. Urban Climate, Vernacular Arch.")
    description = models.TextField()
    impact_metrics = models.CharField(max_length=200, help_text="e.g. -2°C Temp Reduction, 30% Energy Savings")
    image = models.ImageField(upload_to='impact/stories/', blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Impact Stories"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

class ResearchHighlight(models.Model):
    """Research highlights for the Impact page"""
    ICON_CHOICES = [
        ('globe', 'Globe/Earth'),
        ('trending', 'Trending/Growth'),
        ('award', 'Award/Badge'),
        ('check', 'Checkmark/Success'),
    ]
    title = models.CharField(max_length=200)
    icon = models.CharField(max_length=20, choices=ICON_CHOICES, default='globe')
    description = models.TextField()
    link = models.URLField(blank=True, help_text="Link to learn more")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

class PolicyImpact(models.Model):
    """Policy influences for the Impact page"""
    year = models.CharField(max_length=10, help_text="e.g. 2023 or 2021-22")
    title = models.CharField(max_length=200)
    description = models.TextField()
    organization = models.CharField(max_length=200, help_text="e.g. MoHUA, Govt. of India")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-year', 'order']

    def __str__(self):
        return f"{self.year} - {self.title}"
