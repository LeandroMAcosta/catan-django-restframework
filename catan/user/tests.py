from django.test import TestCase
from django.contrib.auth import authenticate
from rest_framework.test import APIRequestFactory

from .models import User
from .views import UserSignup


class UserTestCase(TestCase):
    def setUp(self):
        self.USER_USERNAME = "testuser"
        self.USER_EMAIL = "testuser@test.com"
        self.USER_PASSWORD = "supersecure"

        user_data = {
            "username": self.USER_USERNAME,
            "email": self.USER_EMAIL,
            "password": self.USER_PASSWORD,
        }
        user = User._default_manager.create_user(**user_data)
        user.save()

    def test_authenticate_user(self):
        user = authenticate(
            username=self.USER_USERNAME,
            password=self.USER_PASSWORD
        )
        self.assertNotEqual(user, None)

    def test_bad_authenticate_user(self):
        user = authenticate(
            username=self.USER_USERNAME,
            password=self.USER_PASSWORD+"badpassword"
        )
        self.assertEqual(user, None)

    def test_create(self):

        # Test1: WHITOUT PASS
        factory = APIRequestFactory()
        view = UserSignup.as_view({'post': 'create'})
        request = factory.post('/api/users/')
        response = view(request, 'testuser2', '')
        self.assertEqual(response.status_code, 409)

        # Test2: WHITOUT USER
        factory = APIRequestFactory()
        view = UserSignup.as_view({'post': 'create'})
        request = factory.post('/api/users/')
        response = view(request, '', 'somepassword')
        self.assertEqual(response.status_code, 409)

        # Test3: USER ALREADY EXISTS
        factory = APIRequestFactory()
        view = UserSignup.as_view({'post': 'create'})
        request = factory.post('/api/users/')
        response = view(request, 'testuser', 'somepassword')
        self.assertEqual(response.status_code, 409)

        # Test4: USER create
        factory = APIRequestFactory()
        view = UserSignup.as_view({'post': 'create'})
        request = factory.post('/api/users/')
        response = view(request, 'pepe', 'somepassword')
        self.assertEqual(response.status_code, 201)

    def test_email_alredyexist(self):
        pass
