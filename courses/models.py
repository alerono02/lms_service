from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='курс')
    preview = models.ImageField(max_length=255, upload_to='course', verbose_name='превью', **NULLABLE)
    description = models.TextField(max_length=255, verbose_name='описание', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name='курс')
    preview = models.ImageField(max_length=255, upload_to='course', verbose_name='превью', **NULLABLE)
    description = models.TextField(max_length=255, **NULLABLE, verbose_name='описание')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name='курс')
    video_url = models.URLField(**NULLABLE, verbose_name='ссылка на видео')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
