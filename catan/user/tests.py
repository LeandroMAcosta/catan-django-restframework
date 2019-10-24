from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase

from .models import User
from .views import UserSignup


class UserTestCase(APITestCase):
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

    def test_login_ok(self):
        data = {
            'user': self.USER_USERNAME,
            'pass': self.USER_PASSWORD
        }
        response = self.client.post(
            reverse('login'),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 200)

    def test_login_404(self):
        data = {
            'user': self.USER_USERNAME+"pepito",
            'pass': self.USER_PASSWORD
        }
        response = self.client.post(
            reverse('login'),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 400)

    def test_login_user_empty(self):
        data = {
            'pass': self.USER_PASSWORD
        }
        response = self.client.post(
            reverse('login'),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 400)

    def test_login_pass_empty(self):
        data = {
            'pass': None,
            'user': ''
        }
        response = self.client.post(
            reverse('login'),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 400)
