from django.db import models

class ResearchProject(models.Model):
    """Research and Consultancy Projects - Optimized Model"""
    
    # Status choices
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('planned', 'Upcoming'),
    ]
    
    # Project type choices
    PROJECT_TYPE_CHOICES = [
        ('research', 'Research Project'),
        ('consultancy', 'Consultancy Project'),
    ]
    
    # Role choices
    ROLE_CHOICES = [
        ('pi', 'Principal Investigator (PI)'),
        ('co-pi', 'Co-Principal Investigator (Co-PI)'),
        ('team_member', 'Project Team Member'),
    ]
    
    # === CLASSIFICATION & FILTERING ===
    project_type = models.CharField(
        max_length=20, 
        choices=PROJECT_TYPE_CHOICES, 
        default='research',
        verbose_name="Project Type"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active",
        help_text="Show this project on the public website"
    )
    
    # === CORE INFORMATION ===
    title = models.CharField(
        max_length=500, 
        verbose_name="Project Title"
    )
    description = models.TextField(
        verbose_name="Description",
        help_text="Full project description"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='ongoing',
        verbose_name="Status"
    )
    
    # === FINANCIAL INFORMATION ===
    funding_agency = models.CharField(
        max_length=300, 
        blank=True, 
        verbose_name="Funding Agency / Scheme"
    )
    grant_amount = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Grant / Outlay Amount", 
        help_text="e.g., ₹6.75 L, USD 10,300"
    )

    # === MEDIA & LINKS ===
    image = models.ImageField(
        upload_to='projects/images/',
        blank=True,
        null=True,
        verbose_name="Project Image",
        help_text="Cover image for the project card"
    )
    external_link = models.URLField(
        blank=True,
        verbose_name="External Project URL",
        help_text="Optional: Direct link to project website (overrides detail page)"
    )
    
    # === TEAM INFORMATION ===
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        blank=True,
        verbose_name="Your Role",
        help_text="Your role in this project"
    )
    collaborators = models.TextField(
        blank=True, 
        verbose_name="PI / Collaborators", 
        help_text="Names of principal investigators and collaborators"
    )
    partner_institutions = models.TextField(
        blank=True, 
        verbose_name="Partner Institutions", 
        help_text="Collaborating organizations (e.g., GMDA, TARU, World Bank)"
    )
    
    # === TIMELINE ===
    start_date = models.DateField(
        blank=True, 
        null=True, 
        verbose_name="Start Date"
    )
    end_date = models.DateField(
        blank=True, 
        null=True, 
        verbose_name="End Date"
    )
    
    class Meta:
        verbose_name = "Research Project"
        verbose_name_plural = "Research Projects"
        ordering = ['-start_date']
    
    def __str__(self):
        return self.title
