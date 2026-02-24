from django.db import models
from django.utils import timezone

class ContactSubmission(models.Model):
    """Contact form submissions"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    query = models.TextField()
    submitted_date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    admin_notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"
        ordering = ['-submitted_date']
    
    def __str__(self):
        return f"{self.name} - {self.submitted_date.strftime('%Y-%m-%d %H:%M')}"
