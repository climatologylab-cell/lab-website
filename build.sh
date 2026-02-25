#!/usr/bin/env bash
# Render build script — runs on every deploy
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate --noinput

# Create superuser if it doesn't exist (using env vars)
python manage.py ensure_admin
