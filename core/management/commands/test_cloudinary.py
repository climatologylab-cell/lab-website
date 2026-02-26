"""
Run this on Render Shell to verify Cloudinary credentials:
  python manage.py test_cloudinary
"""
import cloudinary
import cloudinary.api
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Tests Cloudinary credentials by pinging the API"

    def handle(self, *args, **options):
        cfg = settings.CLOUDINARY_STORAGE
        self.stdout.write(f"CLOUD_NAME : {cfg.get('CLOUD_NAME', '(empty)')}")
        self.stdout.write(f"API_KEY    : {cfg.get('API_KEY', '(empty)')}")
        secret = cfg.get("API_SECRET", "")
        if secret:
            self.stdout.write(f"API_SECRET : {secret[:4]}...{secret[-4:]}  (length={len(secret)})")
        else:
            self.stdout.write("API_SECRET : (empty)")

        self.stdout.write("\nTesting connection to Cloudinary...")
        try:
            result = cloudinary.api.ping()
            self.stdout.write(self.style.SUCCESS(f"✅ SUCCESS: {result}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ FAILED: {e}"))
