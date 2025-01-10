#!/bin/bash

# Exit immediately if any command fails
set -e

# Run database migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate


# Start the Django development server
echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000