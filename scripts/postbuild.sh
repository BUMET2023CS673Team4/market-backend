#!/bin/bash
python manage.py makemigrations  # Create migrations for changes to database
python manage.py migrate  # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files