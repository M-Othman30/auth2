#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python ./auth/manage.py flush --no-input
python ./auth/manage.py makemigrations
python ./auth/manage.py migrate
gunicorn auth.wsgi:application --bind 0.0.0.0:8000

exec "$@"