from django.db import models
from django.utils import timezone

class Workshop(models.Model):
    """Notice board workshop entries"""
    title = models.CharField(max_length=300)
    description = models.TextField()
    event_date = models.DateField()
    posted_date = models.DateTimeField(default=timezone.now)
    link = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Workshop/Notice"
        verbose_name_plural = "Workshops/Notices"
        ordering = ['-event_date']
    
    def __str__(self):
        return f"{self.title} - {self.event_date}"
    
    def formatted_date(self):
        return self.event_date.strftime("%b %d, %Y")
