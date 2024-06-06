from datetime import timedelta

from django.db import models
from django.utils import timezone


class User(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def cumulative_time_this_month(self):
        now = timezone.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        logs = Log.objects.filter(user=self, datetime__gte=start_of_month, datetime__lte=now)
        return len(logs) * timedelta(minutes=1)

    def cumulative_time_overall(self):
        logs = Log.objects.filter(user=self)
        return len(logs) * timedelta(minutes=1)

    def __str__(self):
        return self.name


class Device(models.Model):
    mac_address = models.CharField(max_length=17, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    device_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Log(models.Model):
    datetime = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
