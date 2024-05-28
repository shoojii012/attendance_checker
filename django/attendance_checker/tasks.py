from celery import shared_task

@shared_task
def your_task():
    print("Task is running every minute.")