"""
Custom Supabase S3 storage backend.
Uses django-storages[s3] and boto3.
"""
from storages.backends.s3boto3 import S3Boto3Storage

class SupabaseMediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = True
    default_acl = 'public-read'  # Supabase public buckets work best with this
