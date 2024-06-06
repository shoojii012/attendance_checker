import platform
import subprocess as sp
import threading

from celery import shared_task

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
    active_users = {device.user for device in devices if device.mac_address in output}

    for user in User.objects.filter(is_active=True):
        log_attendance(user, now_time, entering=(user in active_users))


def log_attendance(user, now_time, entering):
    Log.objects.create(datetime=now_time, user=user)
    action = "entered" if entering else "exited"
    print(f"{user.name} {action} at {now_time}")
