"""
Custom Supabase S3 storage backend.
Uses django-storages[s3] and boto3.
"""
from storages.backends.s3boto3 import S3Boto3Storage

class SupabaseMediaStorage(S3Boto3Storage):
    location = ''
    file_overwrite = True

