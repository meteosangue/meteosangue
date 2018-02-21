#!/bin/sh
echo 'Migrate database schema'
python manage.py migrate
echo 'Update status'
python manage.py shell -c 'from core.tasks import fetch_and_update; fetch_and_update()'
echo 'Run gunicorn'
exec gunicorn meteosangue.wsgi