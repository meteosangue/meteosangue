from rest_framework import serializers
from core.models import BloodGroup


class BloodGroupSerializer(serializers.ModelSerializer):
    status_expanded = serializers.SerializerMethodField()

    class Meta:
        model = BloodGroup
        fields = ['status', 'status_expanded', 'groupid', 'id']

    def get_status_expanded(self, obj):
        return obj.get_status_display()
