"""
Custom Cloudinary storage backend.

Uses the official `cloudinary` SDK directly — no dependency on the
outdated `django-cloudinary-storage` package.  The `cloudinary` SDK
reads the CLOUDINARY_URL environment variable automatically, so no
extra configuration is required in settings.py.
"""
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


@deconstructible
class CloudinaryMediaStorage(Storage):
    """Drop-in replacement for cloudinary_storage.storage.MediaCloudinaryStorage."""

    def _get_upload_folder(self, name):
        """Return the upload folder derived from the file path."""
        parts = name.replace("\\", "/").split("/")
        return "/".join(parts[:-1]) if len(parts) > 1 else "media"

    def _save(self, name, content):
        folder = self._get_upload_folder(name)
        basename = os.path.splitext(os.path.basename(name))[0]
        result = cloudinary.uploader.upload(
            content,
            folder=folder,
            public_id=basename,
            overwrite=True,
            resource_type="auto",
            use_filename=True,
            unique_filename=False,
        )
        # Store the full public_id so .url() works later
        return result["public_id"]

    def url(self, name):
        if not name:
            return ""
        # If name is already a full URL, return as-is
        if name.startswith("http://") or name.startswith("https://"):
            return name
        return cloudinary.CloudinaryImage(name).build_url(secure=True)

    def exists(self, name):
        # Always allow upload — Cloudinary handles deduplication via overwrite
        return False

    def delete(self, name):
        try:
            cloudinary.uploader.destroy(name, resource_type="image")
        except Exception:
            pass

    def size(self, name):
        try:
            result = cloudinary.api.resource(name)
            return result.get("bytes", 0)
        except Exception:
            return 0

    def _open(self, name, mode="rb"):
        raise NotImplementedError("CloudinaryMediaStorage does not support opening files.")
