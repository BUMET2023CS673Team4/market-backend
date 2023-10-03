#!/bin/bash
# Comment out the following line because the migrations should be created during the developing process
# and the migration codes should be included in the source code repository.
# python manage.py makemigrations  # Create migrations for changes to database
python manage.py migrate  # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files