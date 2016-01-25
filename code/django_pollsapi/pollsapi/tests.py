from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate
from pollsapi.tests.user_setup import setup_user

from pollsapi import views


def setup_user():
    test_user = User.objects.create_user('test', email='testuser@test.com',
                                         password='test')
    test_user.save()
    user = User.objects.get(username='test')
    return user


class TestPoll(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = setup_user()
        self.view = views.PollList.as_view()
        self.uri = '/polls/'

    def test_get(self):
        request = self.factory.get(self.uri)
        force_authenticate(request, self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_post_uri(self):
        params = {
            "question": "How are you man?",
            "choice_strings": ["Yo Man", "Not Fine"],
            "created_by": 1
            }
        request = self.factory.post(self.uri, params)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 201,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))
