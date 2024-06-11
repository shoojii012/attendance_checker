import os
import subprocess as sp

from celery import shared_task

from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone

from .helper import (
    PingThreading,
    cumulative_time_overall,
    cumulative_time_this_month,
    current_users,
)
from .models import Device, Log, User


@shared_task
def check_attendance():
    devices = Device.objects.all()
    thread_list = []

    for i in range(2, 255):
        thread = PingThreading(ip_address=i)
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()

    output = sp.run(["arp", "-a"], capture_output=True, text=True).stdout
    now_time = timezone.now()
    active_users = {
        device.user for device in devices if device.mac_address.lower() in output.lower()
    }

    for user in User.objects.filter(is_active=True):
        if user in active_users:
            Log.objects.create(datetime=now_time, user=user)
            print(f"{user.name} entered at {now_time}")


@shared_task
def generate_statistics_html():
    context = {
        "monthly_ranking": cumulative_time_this_month(),
        "current_users": current_users(),
        "overall_ranking": cumulative_time_overall(),
    }
    html_content = render_to_string("statistics.html", context)
    output_path = os.path.join(settings.BASE_DIR, "attendance_checker", "templates", "index.html")

    with open(output_path, "w") as static_file:
        static_file.write(html_content)

    return output_path
