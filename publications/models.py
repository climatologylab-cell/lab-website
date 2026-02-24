from django.db import models


class Publication(models.Model):
    """Research publications (CSV compatible)"""

    CATEGORY_CHOICES = [
        ('journal', 'Journal Article'),
        ('conference', 'Conference Paper'),
        ('book', 'Book Chapter'),
        ('thesis', 'Thesis'),
        ('report', 'Technical Report'),
        ('guideline', 'Guideline'),
        ('other', 'Other Document'),
    ]

    SCOPE_CHOICES = [
        ('national', 'National'),
        ('international', 'International'),
    ]

    # =========================
    # CSV-MAPPED CORE FIELDS
    # =========================

    # CSV: ID
    csv_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="CSV ID"
    )

    # CSV: PUBLICATIONS (Item)
    title = models.CharField(
        max_length=500
    )

    # CSV: Date
    publication_date = models.DateField(
        null=True,
        blank=True
    )

    # CSV: DATA
    citation = models.TextField(
        blank=True,
        help_text="Full citation/source text (DATA column)"
    )

    # CSV: LINK
    external_link = models.URLField(
        blank=True,
        help_text="External publication link"
    )

    # CSV: PUBLICATIONS(List)
    publication_list = models.CharField(
        max_length=300,
        blank=True
    )

    # CSV: Owner
    owner = models.CharField(
        max_length=200,
        blank=True
    )

    # CSV: Created Date
    created_date = models.DateTimeField(
        blank=True,
        null=True
    )

    # CSV: Updated Date
    updated_date = models.DateTimeField(
        blank=True,
        null=True
    )

    # =========================
    # OPTIONAL / EXISTING FIELDS
    # =========================

    authors = models.CharField(
        max_length=1000,
        blank=True,
        null=True,
        help_text="Comma-separated list of authors"
    )

    related_projects = models.ManyToManyField(
        'projects.ResearchProject',
        blank=True,
        related_name='publications'
    )

    journal = models.CharField(
        max_length=300,
        blank=True,
        help_text="Journal or Conference name"
    )

    volume = models.CharField(max_length=50, blank=True)
    issue = models.CharField(max_length=50, blank=True)
    pages = models.CharField(max_length=50, blank=True)
    doi = models.CharField(max_length=200, blank=True, verbose_name="DOI")
    abstract = models.TextField(blank=True)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='journal'
    )

    scope = models.CharField(
        max_length=20,
        choices=SCOPE_CHOICES,
        blank=True,
        null=True,
        help_text="Scope of the conference (National/International)"
    )

    cover_image = models.ImageField(
        upload_to='publications/covers/',
        blank=True,
        null=True,
        help_text="Cover image for card display"
    )

    pdf_file = models.FileField(
        upload_to='publications/',
        blank=True,
        null=True
    )

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Publication"
        verbose_name_plural = "All Publications"
        ordering = ['-publication_date']

    def __str__(self):
        return self.title

    def formatted_date(self):
        if self.publication_date:
            return self.publication_date.strftime("%d %B %Y")
        return ""


# =========================
# PROXY MODELS (UNCHANGED)
# =========================

class Journal(Publication):
    class Meta:
        proxy = True
        verbose_name = "Journal Article"
        verbose_name_plural = "Journal Articles"


class Conference(Publication):
    class Meta:
        proxy = True
        verbose_name = "Conference Paper"
        verbose_name_plural = "Conference Papers"


class Book(Publication):
    class Meta:
        proxy = True
        verbose_name = "Book Chapter"
        verbose_name_plural = "Book Chapters"


class Guideline(Publication):
    class Meta:
        proxy = True
        verbose_name = "Guideline"
        verbose_name_plural = "Guidelines"


class OtherDocument(Publication):
    class Meta:
        proxy = True
        verbose_name = "Other Document"
        verbose_name_plural = "Other Documents"
