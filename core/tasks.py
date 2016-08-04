from .utils import fetch_blood_groups


"""
Celery tasks to update blood statuses
"""
def fetch_blood_groups_task():
    blood_groups = fetch_blood_groups()
    print (blood_groups)
    return blood_groups