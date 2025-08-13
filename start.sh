#!/bin/bash

# Exit on error
set -e

echo "Starting Django application..."

# Run migrations if database is available
echo "Running database migrations..."
python manage.py migrate --noinput || echo "Migration failed, continuing..."

# Start the server
echo "Starting Gunicorn server..."
exec gunicorn wsgi:application --config gunicorn.conf.py
