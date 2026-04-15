from django.contrib import sitemaps
from django.urls import reverse
from projects.models import ResearchProject

class StaticViewSitemap(sitemaps.Sitemap):
    """Sitemap for high-level static/gallery pages"""
    priority = 1.0
    changefreq = 'weekly'

    def items(self):
        return [
            'core:home', 
            'core:research_projects', 
            'core:consultancy_projects', 
            'core:team', 
            'core:impact', 
            'core:research_technology',
            'core:workshops',
            'core:tutorials',
            'publications:index'
        ]

    def location(self, item):
        return reverse(item)

class ProjectSitemap(sitemaps.Sitemap):
    """Sitemap for individual Research/Consultancy project pages"""
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return ResearchProject.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('core:project_detail', args=[obj.pk])
