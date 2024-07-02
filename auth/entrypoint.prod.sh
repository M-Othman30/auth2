#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
cd ./auth
python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
gunicorn auth.wsgi:application --bind 0.0.0.0:8000

exec "$@"