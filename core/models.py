from __future__ import unicode_literals

import os

from django.conf import settings
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


class Log(models.Model):
    image = models.ImageField(
        upload_to=os.path.join(settings.UPLOAD_ROOT, 'meteo'),
        blank=True
    )
    datetime = models.DateTimeField(unique=True)
    twitter_done = models.BooleanField(default=False)
    facebook_done = models.BooleanField(default=False)
    instagram_done = models.BooleanField(default=False)
