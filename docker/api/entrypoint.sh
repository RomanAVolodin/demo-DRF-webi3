#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"


python manage.py collectstatic --no-input
python manage.py migrate --no-input

DJANGO_SUPERUSER_USERNAME=admin \
	DJANGO_SUPERUSER_PASSWORD=123123 \
	DJANGO_SUPERUSER_EMAIL=mail@mail.ru \
	python manage.py createsuperuser --noinput --name=Adminko || true

gunicorn profiles.wsgi:application --bind 0.0.0.0:8000 --reload

exec "$@"