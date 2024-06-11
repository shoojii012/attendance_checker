from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name=""),
    path("v1/", views.v1, name="v1"),
]
