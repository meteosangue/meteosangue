#!/bin/sh

if [ "$1" = "app" ]; then
    echo 'Migrate database schema'
    until python manage.py migrate; do
        echo 'Retry migrations'
        sleep 1
    done
    echo 'Run gunicorn'
    exec gunicorn meteosangue.wsgi
fi

if [ "$1" = "cron" ]; then
    python manage.py run_huey
fi
