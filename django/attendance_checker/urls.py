from django.urls import path

from . import views

urlpatterns = [
    path("", views.v1, name="v1"),
    path("v2/", views.home, name="home"),
    path("v2/upload-csv/", views.upload_csv, name="upload_csv"),
    path("v2/log-list/", views.log_list, name="log_list"),
    path("v2/user-list/", views.user_list, name="user_list"),
    path("v2/device-list/", views.device_list, name="device_list"),
    path("v2/api/users/", views.api_user_list, name="api_user_list"),
    path(
        "v2/api/create-users-from-csv/",
        views.create_users_from_csv,
        name="create_users_from_csv",
    ),
]
