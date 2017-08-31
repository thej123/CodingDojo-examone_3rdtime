from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^examv3/main$', views.main),
    url(r'^examv3/register$', views.register),
    url(r'^examv3/login$', views.login),
    url(r'^examv3/logout$', views.logout),
]
