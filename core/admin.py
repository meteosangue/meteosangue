from django.contrib import admin

from .models import BloodGroup


@admin.register(BloodGroup)
class BloodGroupAdmin(admin.ModelAdmin):
    pass