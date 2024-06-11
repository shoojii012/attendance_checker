import platform
import subprocess as sp
import threading
from datetime import timedelta

from django.utils import timezone

from .models import Log, User


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
    active_users = {log.user for log in active_logs if log.user is not None}
    sorted_active_users = sorted(active_users, key=lambda user: user.created_at, reverse=True)
    return sorted_active_users
