from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from datetime import datetime
from .models import User, Device, Log
import subprocess as sp

# Djangoの設定モジュールをデフォルトとして設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('attendance_checker')

# Djangoの設定をCeleryに読み込ませる
app.config_from_object('django.conf:settings', namespace='CELERY')

# Djangoのすべてのタスクモジュールをロード
app.autodiscover_tasks()

@app.task(bind=True)
def log_per_minute_task(self):
    # 現在時刻を取得
    now_time = datetime.now()
    print("----------")
    print(now_time)
    print("----------")

    # # arpコマンドでLAN内のデバイスを取得
    # output = (sp.run(["arp", "-a"], capture_output=True, text=True)).stdout

    # # 取得したMACアドレスからユーザーを特定
    # for device in Device.objects.all():
    #     if (
    #         output.find(device.mac_address) != -1
    #     ):
    #         user = device.user
            
    #         # ログテーブルに在室情報を追加
    #         log = Log(datetime=now_time, user=user)
    #         log.save()

    #         # 直前のログを取得
    #         prev_log = Log.objects.filter(user=user).order_by('-datetime')[1]
            
    #         # 直前のログが退室記録の場合、新しいログを作成
    #         if prev_log.is_exit:
    #             log = Log(datetime=now_time, user=user, is_exit=False)
    #             log.save()
            
    #         # 直前のログが在室記録の場合、更新
    #         else:
    #             prev_log.datetime = now_time
    #             prev_log.save()

    # # 10分以上ログがないユーザーを退室処理
    # for user in User.objects.all():
    #     last_log = Log.objects.filter(user=user).order_by('-datetime').first()
    #     if last_log and (now_time - last_log.datetime).total_seconds() > 600:
    #         log = Log(datetime=now_time, user=user, is_exit=True)
    #         log.save()

@app.task(bind=True)
def generate_html(self):
    pass