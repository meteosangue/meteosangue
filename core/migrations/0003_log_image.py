# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-08 16:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='image',
            field=models.ImageField(blank=True, upload_to='/Users/astagi/w/meteosangue/meteosangue/uploads/meteo'),
        ),
    ]