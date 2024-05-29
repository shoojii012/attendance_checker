from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from datetime import datetime

# Djangoの設定モジュールをデフォルトとして設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('attendance_checker')

# Djangoの設定をCeleryに読み込ませる
app.config_from_object('django.conf:settings', namespace='CELERY')

# Djangoのすべてのタスクモジュールをロード
app.autodiscover_tasks()

@app.task(bind=True)
def log_per_minute_task(self):
    nowtime = datetime.now()
    print(f"This is celery task : {nowtime}")
