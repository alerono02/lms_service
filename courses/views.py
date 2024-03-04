from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from courses.filters import PaymentFilter
from courses.models import Course, Lesson, Subscription
from courses.paginators import CoursePaginator, LessonPaginator
from courses.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer
from users.models import Payment
from users.permissions import IsOwner, IsModerator


class CourseViewSet(viewsets.ModelViewSet):

    serializer_class = CourseSerializer
    pagination_class = CoursePaginator
    queryset = Course.objects.all()

    def get_permissions(self):
        """Права доступа"""
        if self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsOwner | IsModerator ]
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

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LessonPaginator
    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(generics.RetrieveAPIView):

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner, IsAuthenticated]


class PaymentViewSet(viewsets.ModelViewSet):

    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        if self.request.user.has_perm(IsAdminUser):
            return Payment.objects.all()
        else:
            return Payment.objects.filter(user=self.request.user)


class SubscribeCourseView(generics.CreateAPIView):
    """
    Создает подписку пользователя на указанный курс.

    Объект ответа с информацией о результате операции.
            HTTP_201_CREATED: Подписка успешно создана.
            HTTP_400_BAD_REQUEST: Подписка уже существует.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        course_id = kwargs.get('course_id')
        course = Course.objects.get(pk=course_id)

        # Проверка, подписан ли пользователь уже на этот курс
        if Subscription.objects.filter(user=request.user, course=course).exists():
            return Response({'detail': 'Вы уже подписаны на этот курс.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={'user': request.user.id, 'course': course.id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({'detail': 'Вы успешно подписались на курс.'}, status=status.HTTP_201_CREATED)


class UnsubscribeCourseView(generics.DestroyAPIView):
    """
    Удаляет подписку пользователя на указанный курс.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        course_id = self.kwargs.get('course_id')
        course = Course.objects.get(pk=course_id)
        return Subscription.objects.get(user=self.request.user, course=course)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Вы успешно отписались от курса.'}, status=status.HTTP_200_OK)
