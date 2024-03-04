from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    '''Тест моделей Course и Lesson'''

    def setUp(self) -> None:
        '''Создается тестовый пользователь'''
        self.user = User.objects.create(
            email='test@mail.ru',
        )
        self.user.set_password('555test555')
        self.user.save()
        self.client.force_authenticate(user=self.user)

        '''Создается тестовый курс'''
        self.course = Course.objects.create(
            title='test course',
            description='test course description',
            owner=self.user
        )

        '''Создается тестовый урок'''
        self.lesson = Lesson.objects.create(
            title='test lesson',
            description='test lesson description',
            video_url='https://www.youtube.com/',
            course=self.course,
            owner=self.user
        )

    def test_list_lesson(self):
        '''Тест READ LIST lesson'''

        self.lesson = Lesson.objects.create(
            title='list test lesson',
            description='list lesson description',
            course=self.course,
            owner=self.user
        )

        response = self.client.get(
            reverse('courses:lesson-list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            Lesson.objects.get(pk=self.lesson.pk).title,
            response.json().get('results')[1].get('title'))

    def test_retrieve_lesson(self):
        '''Тест READ ONE lesson'''
        response = self.client.get(reverse('courses:lesson-get', kwargs={'pk': self.lesson.pk}))

        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
        )

        response = response.json()

        self.assertEqual(response.get('title'), 'test lesson')
        self.assertEqual(response.get('preview'), None)
        self.assertEqual(response.get('description'), 'test lesson description')
        self.assertEqual(response.get('video_url'), 'https://www.youtube.com/')
        self.assertEqual(response.get('course'), self.course.pk)
        self.assertEqual(response.get('owner'), self.user.pk)

    def test_create_lesson(self):
        '''Тест CREATE lesson'''

        data = {
            'title': 'test lesson 2',
            'description': 'description 2',
            'video_url': 'https://www.youtube.com/',
            'course': self.course.pk,
            'owner': self.user.pk,
        }

        lesson_create_url = reverse('courses:lesson-create')
        response = self.client.post(lesson_create_url, data=data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.json().get('title'),
            data.get('title')
        )

        self.assertTrue(
            Lesson.objects.get(pk=self.lesson.pk).title,
            data.get('title')
        )

    def test_update_lesson(self):
        '''Тест UPDATE lesson'''

        data = {
            'title': 'updated lesson',
            'description': 'updated description',
        }

        response = self.client.put(reverse('courses:lesson-update', kwargs={'pk': self.lesson.pk}), data=data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
        )
        response = response.json()

        self.assertEqual(response.get('title'), 'updated lesson')
        self.assertEqual(response.get('description'), 'updated description')
        self.assertEqual(response.get('course'), self.course.pk)
        self.assertEqual(response.get('owner'), self.user.pk)

    def test_delete_lesson(self):
        '''Тест DELETE lesson'''

        response = self.client.delete(reverse('courses:lesson-delete', kwargs={'pk': self.lesson.pk}))

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Lesson.objects.all().exists(),
        )


class SubscriptionTestCase(APITestCase):
    '''Тест модели Subscription'''

    def setUp(self) -> None:
        '''Создается тестовый пользователь'''
        self.user = User.objects.create(
            email='test2@mail.ru',
        )
        self.user.set_password('777test777')
        self.user.save()
        self.client.force_authenticate(user=self.user)

        '''Создается тестовый курс'''
        self.course = Course.objects.create(
            title='test course sub',
            description='test desc sub'
        )

        '''Создание подписки'''
        self.subscription = Subscription.objects.create(
            user=self.user,
            course=self.course,
        )

    def test_subscription(self):
        '''Тест CREATE Subscription'''

        data = {
            'user': self.user.pk,
        }

        subscription_url = reverse('courses:subscribe-course', kwargs={'course_id': self.course.pk})

        response = self.client.post(subscription_url, data=data)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsubscription(self):
        '''Тест unsubscription'''

        data = {
            'user': self.user.pk,
        }

        unsubscription_url = reverse('courses:unsubscribe-course', kwargs={'course_id': self.course.pk})
        response = self.client.delete(unsubscription_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
