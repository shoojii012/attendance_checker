from django.urls import path

from . import views

urlpatterns = [
    path("", views.v1, name="v1"),
    path("v2/", views.home, name="home"),
    path("upload-csv/", views.upload_csv, name="upload_csv"),
    path("log-list/", views.log_list, name="log_list"),
    path("user-list/", views.user_list, name="user_list"),
    path("device-list/", views.device_list, name="device_list"),
    path("api/users/", views.api_user_list, name="api_user_list"),
    path(
        "api/create-users-from-csv/",
        views.create_users_from_csv,
        name="create_users_from_csv",
    ),
    path("create_user/", views.create_user, name="create_user"),
    path("create_device/", views.create_device, name="create_device"),
    path("user_success/", views.user_success, name="user_success"),
    path("device_success/", views.device_success, name="device_success"),
    path("upload_csv/", views.upload_csv, name="upload_csv"),
    path("upload_success/", views.upload_success, name="upload_success"),
]
