# Generated by Django 4.2.7 on 2024-02-15 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='курс')),
                ('preview', models.ImageField(max_length=255, upload_to='course', verbose_name='превью')),
                ('description', models.TextField(blank=True, max_length=255, verbose_name='описание')),
            ],
            options={
                'verbose_name': 'курс',
                'verbose_name_plural': 'курсы',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='курс')),
                ('preview', models.ImageField(max_length=255, upload_to='course', verbose_name='превью')),
                ('description', models.TextField(blank=True, max_length=255, verbose_name='описание')),
                ('video_url', models.URLField()),
            ],
            options={
                'verbose_name': 'урок',
                'verbose_name_plural': 'уроки',
            },
        ),
    ]