import csv
from datetime import datetime
from django.shortcuts import render, redirect
from .models import User, Log, Device
from django.http import JsonResponse


# 　version 1
def v1(request):
    return render(request, 'v1.html')


# version 2
def home(request):
    return render(request, 'home.html')


def task_per_minute(request):

    pass


def upload_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)
        for row in reader:
            name = row[0]
            enter_time = datetime.strptime(row[1], '%Y年%m月%d日 %H:%M')
            leave_time = datetime.strptime(row[2], '%Y年%m月%d日 %H:%M')

            user, _ = User.objects.get_or_create(name=name)
            Log.objects.create(datetime=enter_time, user=user)
            Log.objects.create(datetime=leave_time, user=user)

        return redirect('log_list')
    return render(request, 'upload_csv.html')


def log_list(request):
    logs = Log.objects.all().order_by('datetime')
    return render(request, 'log_list.html', {'logs': logs})


def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})


def device_list(request):
    devices = Device.objects.all()
    return render(request, 'device_list.html', {'devices': devices})


def api_user_list(request):
    users = User.objects.all().values('name', 'is_active', 'created_at', 'updated_at')
    return JsonResponse(list(users), safe=False)
