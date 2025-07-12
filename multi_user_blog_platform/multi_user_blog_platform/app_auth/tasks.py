from celery import shared_task

@shared_task
def return_result():
    return 'It Works'