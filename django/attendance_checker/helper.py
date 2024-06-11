import platform
import subprocess as sp
import threading
from collections import defaultdict
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


# 月末メール送信用
def calculate_user_activity(start_date, end_date):
    users = User.objects.all()
    report_data = defaultdict(list)

    for user in users:
        logs = Log.objects.filter(
            user=user, datetime__gte=start_date, datetime__lte=end_date
        ).order_by("datetime")
        day_logs = defaultdict(list)

        for log in logs:
            log_date = log.datetime.date()
            day_logs[log_date].append(log.datetime)

        for log_date, times in day_logs.items():
            first_entry = times[0]
            last_exit = times[-1]
            report_data[user.name].append((log_date, first_entry, last_exit))

    return report_data
