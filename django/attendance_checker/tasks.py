from datetime import datetime

from celery import shared_task

from .models import Device, Log


@shared_task
def log_per_minute_task():
    # 指定されたファイルのパス
    mac_address_file = "/code/test_mac.txt"
    # ファイルからMACアドレスを読み込む
    with open(mac_address_file, "r") as file:
        mac_addresses = [line.strip() for line in file]
    # 現在時刻を取得
    now = datetime.now()
    # 各MACアドレスに対して処理を実行
    for mac_address in mac_addresses:
        device = Device.objects.get(mac_address=mac_address)
        user = device.user
        Log.objects.create(datetime=now, user=user)
