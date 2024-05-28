from django.urls import path
from . import views

urlpatterns = [
    path('upload-csv/', views.upload_csv, name='upload_csv'),
    path('log-list/', views.log_list, name='log_list'),
    path('user-list/', views.user_list, name='user_list'),
    path('device-list/', views.device_list, name='device_list'),
]