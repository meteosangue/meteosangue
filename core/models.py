from __future__ import unicode_literals

from django.db import models


BLOOD_GROUP_STATUSES = (
    ('U', 'Urgente'),
    ('S', 'Stabile'),
    ('Z', 'Emergenza'),
    ('E', 'Eccedenza'),
)

class BloodGroup(models.Model):
    groupid = models.CharField(max_length=3, unique=True) #AB+, B-, ...
    status = models.CharField(
        max_length=2,
        choices=BLOOD_GROUP_STATUSES,
        default='S',
    ) #choice between U, E ...
