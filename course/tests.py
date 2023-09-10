from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status
from course.models import Course, Lesson, Subscription

from users.models import User

# Create your tests here.


class LessonPositiveTestCase(APITestCase):

    def setUp(self) -> None:

        self.user = User.objects.create(
            email='test@test.com',
        )
        self.user.set_password('test')
        self.user.save()

        self.course = Course.objects.create(
            name='test course',
            description='test course description',
        )

        self.lesson = Lesson.objects.create(
            name='test',
            description='test description',
            url='https://www.youtube.com',
            user=self.user,
            course=self.course,
        )

    def test_create_lesson(self) -> None:

        data = {
            'name': 'test',
            'description': 'test description',
            'url': 'https://www.youtube.com',
            'course': self.course.pk,
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            path='/lesson/create/', data=data,
        )

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED,
        )
        response = response.json()

        self.assertEqual(response.get('name'), 'test')
        self.assertEqual(response.get('description'), 'test description')
        self.assertEqual(response.get('image'), None)
        self.assertEqual(response.get('url'), 'https://www.youtube.com')
        self.assertEqual(response.get('course'), self.course.pk)
        self.assertEqual(response.get('user'), self.user.pk)

        self.assertTrue(
            Lesson.objects.filter(name='test').exists(),
        )

    def test_list_lesson(self) -> None:

        self.client.force_authenticate(user=self.user)

        response = self.client.get('/lesson/')

        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
        )
        response = response.json()

        self.assertEqual(response.get('count'), 1)
        self.assertEqual(response.get('next'), None)
        self.assertEqual(response.get('previous'), None)

        self.assertEqual(response.get('results')[0].get('name'), 'test')
        self.assertEqual(response.get('results')[0].get('description'), 'test description')
        self.assertEqual(response.get('results')[0].get('url'), 'https://www.youtube.com')
        self.assertEqual(response.get('results')[0].get('user'), self.user.pk)
        self.assertEqual(
            response.get('results')[0].get('course'), self.course.pk,
        )
        self.assertEqual(response.get('results')[0].get('image'), None)

    def test_lesson_retrieve(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f'/lesson/{self.lesson.pk}/')

        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
        )
        response = response.json()

        self.assertEqual(response.get('name'), 'test')
        self.assertEqual(response.get('description'), 'test description')
        self.assertEqual(response.get('image'), None)
        self.assertEqual(response.get('url'), 'https://www.youtube.com')
        self.assertEqual(response.get('course'), self.course.pk)
        self.assertEqual(response.get('user'), self.user.pk)

    def test_lesson_update(self):

        self.client.force_authenticate(user=self.user)

        data = {
            'name': 'updated test',
            'description': 'updated test description',
        }

        response = self.client.put(
            path=f'/lesson/update/{self.lesson.pk}/', data=data,
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
        )
        response = response.json()

        self.assertEqual(response.get('name'), 'updated test')
        self.assertEqual(response.get('description'), 'updated test description')
        self.assertEqual(response.get('image'), None)
        self.assertEqual(response.get('url'), 'https://www.youtube.com')
        self.assertEqual(response.get('course'), self.course.pk)
        self.assertEqual(response.get('user'), self.user.pk)

    def test_lesson_delete(self):

        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            f'/lesson/delet/{self.lesson.pk}/',
        )

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Lesson.objects.all().exists(),
        )

    def tearDown(self) -> None:
        self.user.delete()
        self.course.delete()
        self.lesson.delete()


class LessonNegativeTestCase(APITestCase):

    def setUp(self) -> None:

        self.user = User.objects.create(
            email='test@test.com',
        )
        self.user.set_password('test')
        self.user.save()

        self.course = Course.objects.create(
            name='test course',
            description='test course description',
        )

    def test_lesson_create_wrong_url(self):

        data = {
            'name': 'test',
            'description': 'test description',
            'url': 'https://www.qwe.com',
            'course': self.course.pk,
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            path='/lesson/create/', data=data,
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
        )

    def test_lesson_create_wrong_url_field(self):

        data = {
            'name': 'test',
            'description': 'https://www.qwe.com',
            'course': self.course.pk,
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            path='/lesson/create/', data=data,
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
        )

class SubscriptionPositiveTestCase(APITestCase):

    def setUp(self) -> None:

        self.user = User.objects.create(
            email='test@test.com',
        )
        self.user.set_password('test')
        self.user.save()

        self.course = Course.objects.create(
            name='test course',
            description='test course description',
        )

        self.lesson = Lesson.objects.create(
            name='test',
            description='test description',
            url='https://www.youtube.com',
            user=self.user,
            course=self.course,
        )

    def test_subscription_create(self):

        self.client.force_authenticate(user=self.user)

        data = {
            'course': self.course.pk,
            'user': self.user.pk,
        }

        response = self.client.post(
            path='/user/sub/create/', data=data,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('course'), self.course.pk)
        self.assertEqual(response.json().get('user'), self.user.pk)
        self.assertEqual(response.json().get('course_name'), self.course.name)

    def test_subscription_delete(self):

        subscription = Subscription.objects.create(
            course=self.course,
            user=self.user,
        )

        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            f'/user/sub/delete/{subscription.pk}/',
        )

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Subscription.objects.all().exists(),
        )
