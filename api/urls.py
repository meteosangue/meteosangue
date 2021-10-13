from .views import BloodGroupViewSet

from django.urls import path, re_path


urlpatterns = [
    path('bloodgroups/', BloodGroupViewSet.as_view({'get': 'list'}), name='bloodgroups'),
    re_path(r'^bloodgroups/(?P<group_id>(A|B|AB|O)(\-|\+))/$',
                    BloodGroupViewSet.as_view({'get': 'retrieve'}), name='bloodgroup')
]
