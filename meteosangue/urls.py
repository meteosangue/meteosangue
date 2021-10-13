"""meteosangue URL Configuration"""
from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    path('admin', admin.site.urls),
    path('api/', include('api.urls')),
]