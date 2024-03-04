from django.contrib import admin

from courses.models import Course, Lesson


# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'description',)
    list_filter = ('id',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'description', 'course',)
    list_filter = ('id',)