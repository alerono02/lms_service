from django.contrib.auth.models import AbstractUser
from django.db import models
from courses.models import NULLABLE, Course, Lesson


class User(AbstractUser):
    username = None

    email = models.EmailField(max_length=150, unique=True, verbose_name='Email')
    phone = models.CharField(max_length=35, verbose_name='номер телефона', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='город', **NULLABLE)
    avatar = models.ImageField(upload_to='users', verbose_name='аватар', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Payment(models.Model):
    PAYMENT_METHODS = (
        (1, 'Наличными'),
        (2, 'Безналичными'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)
    date = models.DateField(verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок', **NULLABLE)
    price = models.PositiveIntegerField(verbose_name='Стоимость')
    payment_method = models.CharField(choices=PAYMENT_METHODS, verbose_name='Способ оплаты')

    class Meta:

        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
