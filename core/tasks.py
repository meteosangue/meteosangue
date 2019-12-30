import time
import redis

from django.conf import settings

from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from .models import Log
from .main import post_blood_weather, update_blood_groups


"""
Method to fetch blood groups and update status
"""
def fetch_and_update():
    blood_groups, log = update_blood_groups()
    post_blood_weather(blood_groups, log)


"""
Periodic task to update blood statuses
"""
@db_periodic_task(crontab(minute='*/15'))
def main_blood_groups_task():
    fetch_and_update()
    time.sleep(settings.BLOOD_FETCH_INTERVAL)
    return True

