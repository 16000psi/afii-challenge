#!/bin/sh

echo "Applying database migrations"
python manage.py migrate --settings envirotrade.settings.prod

echo "Populating database with test data"
python manage.py generate_dummy_data --settings envirotrade.settings.prod

echo "Collecting static files"
python manage.py collectstatic --noinput --settings envirotrade.settings.prod

# Start the server
exec "$@"

