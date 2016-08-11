import time
from django_rq import job

from .models import Log
from .main import post_blood_weather, update_blood_groups


"""
Method to fetch blood groups and update status
"""
def fetch_and_update():
    blood_groups, log = update_blood_groups()
    post_blood_weather(blood_groups, log)


"""
RQ job to update blood statuses
"""
@job
def main_blood_groups_task():
    while True:
        fetch_and_update()
        time.sleep(60 * 15)


main_blood_groups_task.delay()
