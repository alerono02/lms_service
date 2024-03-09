from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.filters import PaymentFilter
from courses.models import Course, Lesson, Subscription
from courses.paginators import CoursePaginator, LessonPaginator
from courses.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer
from users.models import Payment
from users.permissions import IsOwner, IsModerator
from users.serializers import UserSerializer
from users.services import get_session


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для взаимодействия с моделью курса.
    """

    serializer_class = CourseSerializer
    pagination_class = CoursePaginator
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_permissions(self):
        """Права доступа"""
        if self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'destroy':
            permission_classes = [IsOwner, IsAuthenticated]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        else:
            permission_classes = [IsAuthenticated | IsModerator]
        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    """Create a Lesson"""

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """List of lessons"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LessonPaginator
    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Lesson view"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Lesson update"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Lesson destroy"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner, IsAuthenticated]


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet for payment"""
    queryset = Payment.objects.all()

    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        paid_of_course = serializer.save()
        stripe_obj = get_session(paid_of_course)
        paid_of_course.stripe_link = stripe_obj.url
        paid_of_course.stripe_id = stripe_obj.id
        paid_of_course.save()


class SubscriptionView(APIView):
    queryset = Course.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            try:
                course = Course.objects.get(owner=self.request.user)
            except:
                course = None

            if course is None:
                HttpResponseRedirect(reverse("course"))

        else:
            course_id = self.request.session.get("course_id")
            if course_id is None:
                HttpResponseRedirect(reverse("course"))

            course = Course.objects.get(id=course_id)

        return course

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user_data = UserSerializer(user).data

        course_id = request.data.get('course_id')

        if course_id is None:
            return Response({"message": "Отсутствует идентификатор курса в запросе"}, status=400)

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise Http404("Курс с таким идентификатором не найден")

        subs_item = Subscription.objects.filter(user=user, course=course)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка на курс удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка на курс добавлена'

        return Response({"message": message, "user": user_data})
