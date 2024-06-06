import csv
from datetime import datetime, timedelta

from django.http import JsonResponse
from django.shortcuts import redirect, render

from .forms import CSVUploadForm, DeviceForm, UserForm
from .models import Device, Log, User


def user_monthly_hours(request):
    now = datetime.now()
    start_of_month = datetime(now.year, now.month, 1)

    users = User.objects.all()
    user_data = []

    for user in users:
        logs = Log.objects.filter(user=user, datetime__gte=start_of_month, datetime__lt=now)

        total_seconds = 0
        for log in logs:
            if log.created_at and log.updated_at:
                total_seconds += (log.updated_at - log.created_at).total_seconds()

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        user_data.append(
            {
                "name": user.name,
                "hours": hours,
                "minutes": minutes,
            }
        )

    return render(request, "user_monthly_hours.html", {"user_data": user_data})


def upload_csv(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["csv_file"]
            file_data = csv_file.read().decode("utf-8")
            csv_data = csv.reader(file_data.splitlines())

            for row in csv_data:
                name = row[0]
                try:
                    enter_time = datetime.strptime(row[1], "%Y年%m月%d日 %H:%M")
                    exit_time = datetime.strptime(row[2], "%Y年%m月%d日 %H:%M")
                except ValueError:
                    # 日付フォーマットが正しくない場合、スキップ
                    continue

                # 入室時間が退出時間より後の場合、その行をスキップ
                if enter_time > exit_time:
                    continue

                user, created = User.objects.get_or_create(name=name)

                current_time = enter_time
                while current_time <= exit_time:
                    Log.objects.create(datetime=current_time, user=user)
                    current_time += timedelta(minutes=1)

            return redirect("upload_success")
    else:
        form = CSVUploadForm()

    return render(request, "upload_csv.html", {"form": form})


# def upload_csv(request):
#     if request.method == "POST":
#         form = CSVUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             csv_file = request.FILES["csv_file"]
#             file_data = csv_file.read().decode("utf-8")
#             csv_data = csv.reader(file_data.splitlines())
#             next(csv_data)  # Skip the header row

#             for row in csv_data:
#                 name = row[0]
#                 mac_addresses = row[1:]
#                 user, created = User.objects.get_or_create(name=name)

#                 for mac in mac_addresses:
#                     if mac and mac.strip():  # Skip empty or None MAC addresses
#                         try:
#                             Device.objects.get_or_create(mac_address=mac.strip(), user=user)
#                         except IntegrityError:
#                             pass  # Handle the case where the mac_address is already in the database

#             return redirect("upload_success")
#     else:
#         form = CSVUploadForm()

#     return render(request, "upload_csv.html", {"form": form})


def upload_success(request):
    return render(request, "success.html", {"message": "CSV file processed successfully!"})


# 　version 1
def v1(request):
    return render(request, "v1.html")


# version 2
def home(request):
    return render(request, "home.html")


def create_user(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect("user_success")
    else:
        user_form = UserForm()
    return render(request, "create_user.html", {"user_form": user_form})


def create_device(request):
    if request.method == "POST":
        device_form = DeviceForm(request.POST)
        if device_form.is_valid():
            device_form.save()
            return redirect("device_success")
    else:
        device_form = DeviceForm()
    return render(request, "create_device.html", {"device_form": device_form})


def user_success(request):
    return render(request, "success.html", {"message": "User created successfully!"})


def device_success(request):
    return render(request, "success.html", {"message": "Device created successfully!"})


# def upload_csv(request):
#     if request.method == "POST" and request.FILES["csv_file"]:
#         csv_file = request.FILES["csv_file"]
#         decoded_file = csv_file.read().decode("utf-8").splitlines()
#         reader = csv.reader(decoded_file)
#         for row in reader:
#             name = row[0]
#             enter_time = datetime.strptime(row[1], "%Y年%m月%d日 %H:%M")
#             leave_time = datetime.strptime(row[2], "%Y年%m月%d日 %H:%M")

#             user, _ = User.objects.get_or_create(name=name)
#             Log.objects.create(datetime=enter_time, user=user)
#             Log.objects.create(datetime=leave_time, user=user)

#         return redirect("log_list")
#     return render(request, "upload_csv.html")


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
