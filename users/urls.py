from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter

from courses.views import PaymentViewSet
from users.views import UserCreate

app_name = UsersConfig.name

router = DefaultRouter()
router.register('payments', PaymentViewSet, basename='payments')


urlpatterns = [
    path('create/', UserCreate.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
