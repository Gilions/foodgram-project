#!/bin/sh
python manage.py migrate
python manage.py createcachetable
python manage.py collectstatic  --noinput
gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
exec "$@"