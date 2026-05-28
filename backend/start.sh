#!/sh
echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Starting Celery worker..."
celery -A core worker -l info --detach

echo "Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:${PORT:-8000} core.wsgi:application
