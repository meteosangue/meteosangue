#!/bin/sh

echo 'Migrate database schema'
until python manage.py migrate; do
    echo 'Retry migrations'
    sleep 1
done
echo 'Update status'
python manage.py shell -c 'from core.tasks import fetch_and_update; fetch_and_update()'
echo 'Run cron in background'
python manage.py rqworker  &
echo 'Run gunicorn'
exec gunicorn meteosangue.wsgi
