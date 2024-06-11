from django.shortcuts import render

from .models import Device, User


def home(request):
    return render(request, "index.html")


def v1(request):
    return render(request, "v1.html")


def user_list(request):
    users = User.objects.all()
    return render(request, "user_list.html", {"users": users})


def device_list(request):
    devices = Device.objects.all()
    return render(request, "device_list.html", {"devices": devices})
