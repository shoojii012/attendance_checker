import csv
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .decorators import admin_required
from .forms import DeviceForm, UserForm
from .models import Device, Log, User


# 　version 1
def v1(request):
    return render(request, "v1.html")


# version 2
def home(request):
    return render(request, "home.html")


@login_required
@admin_required
def create_user(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect("user_success")
    else:
        user_form = UserForm()
    return render(request, "create_user.html", {"user_form": user_form})


@login_required
@admin_required
def create_device(request):
    if request.method == "POST":
        device_form = DeviceForm(request.POST)
        if device_form.is_valid():
            device_form.save()
            return redirect("device_success")
    else:
        device_form = DeviceForm()
    return render(request, "create_device.html", {"device_form": device_form})


@login_required
@admin_required
def user_success(request):
    return render(request, "success.html", {"message": "User created successfully!"})


@login_required
@admin_required
def device_success(request):
    return render(request, "success.html", {"message": "Device created successfully!"})


def upload_csv(request):
    if request.method == "POST" and request.FILES["csv_file"]:
        csv_file = request.FILES["csv_file"]
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.reader(decoded_file)
        for row in reader:
            name = row[0]
            enter_time = datetime.strptime(row[1], "%Y年%m月%d日 %H:%M")
            leave_time = datetime.strptime(row[2], "%Y年%m月%d日 %H:%M")

            user, _ = User.objects.get_or_create(name=name)
            Log.objects.create(datetime=enter_time, user=user)
            Log.objects.create(datetime=leave_time, user=user)

        return redirect("log_list")
    return render(request, "upload_csv.html")


def log_list(request):
    logs = Log.objects.all().order_by("datetime")
    return render(request, "log_list.html", {"logs": logs})


def user_list(request):
    users = User.objects.all()
    return render(request, "user_list.html", {"users": users})


def device_list(request):
    devices = Device.objects.all()
    return render(request, "device_list.html", {"devices": devices})


def api_user_list(request):
    users = User.objects.all().values("name", "is_active", "created_at", "updated_at")
    return JsonResponse(list(users), safe=False)


def create_users_from_csv(request):
    if request.method == "POST" and request.FILES["csv_file"]:
        csv_file = request.FILES["csv_file"]
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.reader(decoded_file)
        for row in reader:
            name = row[0]
            is_active = row[1].lower() == "true"
            User.objects.get_or_create(name=name, defaults={"is_active": is_active})
        return redirect("user_list")
    return render(request, "upload_users_csv.html")
