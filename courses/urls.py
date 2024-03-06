from django.urls import path

from courses.apps import CoursesConfig
from rest_framework.routers import DefaultRouter

from courses.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, SubscribeCourseView, UnsubscribeCourseView, PaymentViewSet

app_name = CoursesConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register('payments', PaymentViewSet, basename='payments')

urlpatterns = [
    path('lesson/create', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>', LessonRetrieveAPIView.as_view(), name='lesson-get'),
    path('lesson/update/<int:pk>', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    path('subscribe/<int:course_id>/', SubscribeCourseView.as_view(), name='subscribe-course'),
    path('unsubscribe/<int:course_id>/', UnsubscribeCourseView.as_view(), name='unsubscribe-course'),
] + router.urls
