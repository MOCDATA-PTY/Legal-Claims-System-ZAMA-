#!/bin/bash
echo "Running server"
PORT=${PORT:-8000}

# Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run gunicorn server
echo "Starting gunicorn server..."
gunicorn university.wsgi:application --bind 0.0.0.0:$PORT
