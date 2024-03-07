from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from courses.models import Course, Lesson, Subscription
from courses.validators import LessonValidator
from users.models import Payment, User
from users.services import create_payment, retrieve_payment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LessonValidator(field='video_url')]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["course", "user"]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.IntegerField(source='lesson_set.count', read_only=True)
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_is_subscribed(self, obj):
        # Получаем текущего пользователя из запроса
        user = self.context['request'].user

        for sub in Subscription.objects.filter(user=user, course=obj.pk):
            if sub.user == user:
                return True
        return False

    class Meta:
        model = Course
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

    def get_payment_stripe(self, instance):

        request = self.context.get('request')

        if request.stream.method == 'POST':
            stripe_id = create_payment(int(instance.payment_amount))
            obj_payments = Payment.objects.get(id=instance.id)
            obj_payments.stripe_id = stripe_id
            obj_payments.save()
            return retrieve_payment(stripe_id)
        if request.stream.method == 'GET':
            if not instance.stripe_id:
                return None
            return retrieve_payment(instance.stripe_id)
