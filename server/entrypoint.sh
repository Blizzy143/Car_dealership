#!/bin/sh

# Make migrations and apply them
echo "Making migrations and migrating the database."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Execute the CMD
exec "$@"