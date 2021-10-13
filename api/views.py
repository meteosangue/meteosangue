from .serializers import BloodGroupSerializer
from core.models import BloodGroup

from rest_framework import viewsets
from rest_framework.response import Response

BLOODS_DOES_NOT_EXIST = "Empty database, sorry"
BLOOD_DOES_NOT_EXIST = "This Blood Group does not exist"


class BloodGroupViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        try:
            all_blood_groups = BloodGroup.objects.all()
            serialized_groups = BloodGroupSerializer(
                all_blood_groups, many=True)
            return Response(serialized_groups.data, status=200)
        except BloodGroup.DoesNotExist:
            return Response(BLOODS_DOES_NOT_EXIST, status=404)

    def retrieve(self, request, *args, **kwargs):
        try:
            blood_group = BloodGroup.objects.get(groupid=kwargs['group_id'])
            serialized_group = BloodGroupSerializer(blood_group)

            return Response(serialized_group.data, status=200)
        except BloodGroup.DoesNotExist:
            return Response(BLOOD_DOES_NOT_EXIST, status=404)
