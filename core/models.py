import datetime

from django.conf import settings
from django.db import models


BLOOD_GROUP_STATUSES = (
    ('U', 'Urgente'),
    ('S', 'Stabile'),
    ('Z', 'Emergenza'),
    ('E', 'Eccedenza'),
    ('F', 'Fragile'),
)


class BloodGroup(models.Model):
    groupid = models.CharField(max_length=3, unique=True)  # AB+, B-, ...
    status = models.CharField(
        max_length=2,
        choices=BLOOD_GROUP_STATUSES,
        default='S',
    )  # choice between U, E ...

    def __str__(self):
        return self.groupid


class Log(models.Model):
    datetime = models.DateTimeField(unique=True)
    image = models.ImageField(
        upload_to=settings.UPLOAD_METEO,
        blank=True
    )
    twitter_done = models.BooleanField(default=False)
    telegram_done = models.BooleanField(default=False)
    facebook_done = models.BooleanField(default=False)

    @property
    def is_completed(self):
        return self.twitter_done and self.telegram_done and self.facebook_done

    def __str__(self):
        if self.datetime:
            return self.datetime.replace(microsecond=0).isoformat()
        else:
            return 'Bad Log entry'
