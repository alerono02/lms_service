from django.urls import path

from courses.apps import CoursesConfig
from rest_framework.routers import DefaultRouter

from courses.views import PaymentViewSet

app_name = CoursesConfig.name

router = DefaultRouter()
router.register('payments', PaymentViewSet, basename='payments')

urlpatterns = [
] + router.urls
