from .models import Log
from .utils import post_blood_weather, update_blood_groups


"""
Celery tasks to update blood statuses
"""
def main_blood_groups_task():
    blood_groups, log = update_blood_groups()
    post_blood_weather(blood_groups, log)