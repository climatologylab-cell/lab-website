"""
Run this on Render Shell to verify Supabase Storage credentials:
  python manage.py test_supabase
"""
import boto3
from botocore.config import Config
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Tests Supabase Storage credentials by checking bucket access"

    def handle(self, *args, **options):
        endpoint = settings.AWS_S3_ENDPOINT_URL
        region = settings.AWS_S3_REGION_NAME
        access_key = settings.AWS_S3_ACCESS_KEY_ID
        secret_key = settings.AWS_S3_SECRET_ACCESS_KEY
        bucket = settings.AWS_STORAGE_BUCKET_NAME

        self.stdout.write(f"ENDPOINT   : {endpoint or '(empty)'}")
        self.stdout.write(f"REGION     : {region or '(empty)'}")
        self.stdout.write(f"ACCESS_KEY : {access_key or '(empty)'}")
        
        if secret_key:
            self.stdout.write(f"SECRET_KEY : {secret_key[:4]}...{secret_key[-4:]}  (length={len(secret_key)})")
        else:
            self.stdout.write("SECRET_KEY : (empty)")
            
        self.stdout.write(f"BUCKET     : {bucket or '(empty)'}")

        self.stdout.write("\nTesting connection to Supabase S3...")
        try:
            s3 = boto3.client(
                's3',
                endpoint_url=endpoint,
                region_name=region,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                config=Config(signature_version='s3v4')
            )
            s3.head_bucket(Bucket=bucket)
            self.stdout.write(self.style.SUCCESS(f"✅ SUCCESS: Connected to bucket '{bucket}'"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ FAILED: {e}"))
