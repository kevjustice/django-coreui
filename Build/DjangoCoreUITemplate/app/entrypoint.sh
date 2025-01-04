#!/bin/bash

pip install --no-cache-dir -r /requirements.txt 

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
#python manage.py initial_setup

# Start server
python manage.py runserver 0.0.0.0:8000
