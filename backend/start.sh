#!/bin/sh

set -e

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."

exec gunicorn \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 300 \
    core.wsgi:application