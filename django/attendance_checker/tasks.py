import platform
import subprocess as sp
import threading

from celery import shared_task

from django.utils import timezone

from .models import Device, Log, User


class PingThreading(threading.Thread):
    def __init__(self, ip_address):
        self.ip_address = ip_address
        threading.Thread.__init__(self)

    def run(self):
        if platform.system() == "Linux":
            sp.run(["ping", "-c", "1", "-w", "1", "192.168.10." + str(self.ip_address)])
        elif platform.system() == "Darwin":
            sp.run(["ping", "-c", "1", "-W", "1", "192.168.10." + str(self.ip_address)])
        else:
            print("Unsupported OS")


@shared_task
def check_attendance():
    devices = Device.objects.all()

    # arpによるLAN環境下のデバイスの取得
    thread_list = []
    for i in range(2, 255):
        thread = PingThreading(ip_address=i)
        thread.start()
        thread_list.append(thread)
    for thread in thread_list:
        thread.join()
    output = (sp.run(["arp", "-a"], capture_output=True, text=True)).stdout

    now_time = timezone.now()
    active_users = set()

    for device in devices:
        if device.mac_address in output:
            active_users.add(device.user)
            log_attendance(device.user, now_time, entering=True)

    update_attendance(active_users, now_time)


def log_attendance(user, now_time, entering):
    if entering:
        Log.objects.create(datetime=now_time, user=user)
        print(f"{user.name} entered at {now_time}")
    else:
        Log.objects.create(datetime=now_time, user=user)
        print(f"{user.name} exited at {now_time}")


def update_attendance(active_users, now_time):
    all_users = User.objects.filter(is_active=True)
    for user in all_users:
        if user in active_users:
            # ユーザーが現在アクティブなら何もしない
            pass
        else:
            # ユーザーがアクティブでないなら、退出ログを記録
            log_attendance(user, now_time, entering=False)
