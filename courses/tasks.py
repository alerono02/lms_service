import json
from datetime import datetime, timedelta
from celery import shared_task
from django.core.mail import send_mail

from django_celery_beat.models import PeriodicTask, IntervalSchedule

from config import settings
from courses.models import Course, Subscription


@shared_task
def send_update_course(course_id):
    '''Отложенная задача - рассылка на обновления материалов курса'''
    course = Course.objects.get(pk=course_id)
    course_sub = Subscription.objects.filter(course=course_id)
    for sub in course_sub:
        send_mail(subject=f"{course.title}",
                  message=f"Обновление {course.title}",
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[f'{sub.user}'],
                  fail_silently=True
                  )



# Создаем интервал для повтора
schedule, created = IntervalSchedule.objects.get_or_create(
    every=10,
    period=IntervalSchedule.SECONDS,
)

# Создаем задачу для повторения
PeriodicTask.objects.create(
    interval=schedule,
    name='Importing contacts',
    task='proj.tasks.import_contacts',
    args=json.dumps(['arg1', 'arg2']),
    kwargs=json.dumps({
        'be_careful': True,
    }),
    expires=datetime.utcnow() + timedelta(seconds=30)
)
