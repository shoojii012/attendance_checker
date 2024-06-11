import os
import subprocess as sp
from datetime import timedelta

from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from .helper import (
    PingThreading,
    calculate_user_activity,
    cumulative_time_overall,
    cumulative_time_this_month,
    current_users,
)
from .models import Device, Log, User


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


@shared_task
def generate_statistics_html():
    context = {
        "monthly_ranking": cumulative_time_this_month(),
        "current_users": current_users(),
        "overall_ranking": cumulative_time_overall(),
    }
    html_content = render_to_string("statistics.html", context)
    output_path = os.path.join(settings.BASE_DIR, "attendance_checker", "templates", "index.html")

    with open(output_path, "w") as static_file:
        static_file.write(html_content)

    return output_path


@shared_task
def send_monthly_report():
    now = timezone.now()
    first_day_of_current_month = now.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_previous_month = last_day_of_previous_month.replace(day=1)

    report_data = calculate_user_activity(first_day_of_previous_month, last_day_of_previous_month)

    email_content = "Monthly Report\n\n"
    for user_name, entries in report_data.items():
        email_content += f"User: {user_name}\n"
        for entry in entries:
            email_content += f"Date: {entry[0]}, First Entry: {entry[1]}, Last Exit: {entry[2]}\n"
        email_content += "\n"

    send_mail(
        "Monthly User Activity Report",
        email_content,
        settings.DEFAULT_FROM_EMAIL,
        ["to@example.com"],
        fail_silently=False,
    )
