from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^examv3/travels$', views.travels),
    url(r'^examv3/register$', views.register),
    url(r'^examv3/login$', views.login),
    url(r'^examv3/logout$', views.logout),
    url(r'^examv3/home$', views.home),
    url(r'^examv3/travels/add$', views.travels_add),
    url(r'^examv3/add/trip$', views.add_trip),
    url(r'^examv3/join/(?P<trip_id>\d+)$', views.join_trip),
    url(r'^examv3/destination/(?P<trip_id>\d+)$', views.destination),
]
