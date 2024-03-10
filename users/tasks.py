from celery import shared_task
from datetime import timedelta
from django.utils import timezone

from users.models import User


@shared_task()
def user_activity_check():
    '''Периодическая задача - проверка активности пользователя (если нет активности 30 дней - блокировка)'''
    users = User.objects.all()
    for user in users:
        if user.last_login:
            if timezone.now() - user.last_login > timedelta(days=30):  # если не активен более 30 дней
                user.is_active = False  # деактивировать
                user.save()