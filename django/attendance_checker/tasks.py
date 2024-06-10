import os
import platform
import subprocess as sp
import threading
from datetime import timedelta

from celery import shared_task

from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone

from .models import Device, Log, User


class PingThreading(threading.Thread):
    def __init__(self, ip_address):
        super().__init__()
        self.ip_address = ip_address

    def run(self):
        if platform.system() == "Linux":
            sp.run(["ping", "-c", "1", "-w", "1", f"192.168.10.{self.ip_address}"])
        elif platform.system() == "Darwin":
            sp.run(["ping", "-c", "1", "-W", "1", f"192.168.10.{self.ip_address}"])
        else:
            print("Unsupported OS")


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


def cumulative_time_this_month():
    users = User.objects.all()
    user_times = [(user, user.cumulative_time_this_month()) for user in users]
    user_times.sort(key=lambda x: x[1], reverse=True)
    return user_times


def cumulative_time_overall():
    users = User.objects.all()
    user_times = [(user, user.cumulative_time_overall()) for user in users]
    user_times.sort(key=lambda x: x[1], reverse=True)
    return user_times


def current_users():
    now = timezone.now()
    active_logs = Log.objects.filter(datetime__gte=now - timedelta(minutes=1))
    active_users = {log.user for log in active_logs}
    return active_users


@shared_task
def generate_statistics_html():
    context = {
        "monthly_ranking": cumulative_time_this_month(),
        "current_users": current_users(),
        "overall_ranking": cumulative_time_overall(),
    }
    html_content = render_to_string("statistics.html", context)
    output_path = os.path.join(settings.BASE_DIR, "static", "statistics.html")

    with open(output_path, "w") as static_file:
        static_file.write(html_content)

    return output_path
