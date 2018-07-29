from django.contrib import admin

from .models import BloodGroup, Log


@admin.register(BloodGroup)
class BloodGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Log)
class LogGroupAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_completed')

    def is_completed(self, obj):
        return obj.is_completed
    is_completed.boolean = True
