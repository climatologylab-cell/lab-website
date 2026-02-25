from django.core.management.base import BaseCommand
from core.models import RTNotice
from datetime import date

class Command(BaseCommand):
    help = 'Adds sample Research and Technology notices'

    def handle(self, *args, **options):
        samples = [
            {
                'notice_type': 'Research',
                'title': 'Urban Climate Resilience Study',
                'description': 'A comprehensive research initiative focusing on urban heat island effects and mitigation strategies in metropolitan areas of India.',
                'event_date': date(2025, 2, 1),
                'link': 'https://example.com/research-resilience',
                'is_active': True,
            },
            {
                'notice_type': 'Research',
                'title': 'Monsoon Pattern Variability Analysis',
                'description': 'Exploring the socio-economic impacts of changing monsoon patterns across the Indo-Gangetic plains using advanced meteorological datasets.',
                'event_date': date(2025, 1, 15),
                'link': 'https://example.com/monsoon-study',
                'is_active': True,
            },
            {
                'notice_type': 'Technology',
                'title': 'IoT-Based Real-time Air Quality Network',
                'description': 'Deployment of a high-density sensor network for real-time monitoring of PM2.5 and PM10 levels for urban planning.',
                'event_date': date(2025, 2, 10),
                'link': 'https://example.com/air-monitor',
                'is_active': True,
            },
            {
                'notice_type': 'Technology',
                'title': 'AI-Powered Satellite Drought Detection',
                'description': 'Implementation of a machine learning framework that processes Sentinel-2 imagery to detect early signs of agricultural drought.',
                'event_date': date(2025, 2, 20),
                'link': 'https://example.com/drought-ai',
                'is_active': True,
            },
        ]

        for s in samples:
            notice, created = RTNotice.objects.get_or_create(
                title=s['title'],
                defaults=s
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created {s['notice_type']}: {s['title']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Skipped: {s['title']} (already exists)"))
