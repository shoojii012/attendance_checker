from __future__ import absolute_import, unicode_literals

# Celeryアプリケーションをインポートして設定
from .celery import app

__all__ = ('app',)
