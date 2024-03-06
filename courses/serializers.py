from rest_framework import serializers

from courses.models import Course, Lesson, Subscription
from courses.validators import LessonValidator
from users.models import Payment
from users.services import create_payment, retrieve_payment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LessonValidator(field='video_url')]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.IntegerField(source='lesson_set.count', read_only=True)
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)

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


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
