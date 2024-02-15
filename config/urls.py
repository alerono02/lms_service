from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('courses.urls', namespace='courses'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
