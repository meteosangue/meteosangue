from .views import BloodGroupViewSet

from django.conf.urls import include
from django.conf.urls import url
from rest_framework import routers
router = routers.DefaultRouter()


router.register(r'bloodgroups', BloodGroupViewSet, 'bloodgroups')
router.register(r'bloodgroups/?P<group_id>[[0-9]|[(A|B|AB|O)[-+]]]+',
                BloodGroupViewSet.retrieve, 'bloodgroup')


urlpatterns = [
    url(r'^', include(router.urls)),
]
