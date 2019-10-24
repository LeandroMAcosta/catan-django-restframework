from django.urls import reverse
from rest_framework.test import APITestCase

from .models import User


class UserTestCase(APITestCase):
    def setUp(self):
        self.USER_USERNAME = "testuser"
        self.USER_PASSWORD = "supersecure"

        self.USER_USERNAME2 = "testuser2"
        self.USER_PASSWORD2 = "supersecure2"

        user_data = {
            "username": self.USER_USERNAME,
            "password": self.USER_PASSWORD,
        }
        user = User._default_manager.create_user(**user_data)
        user.save()

    def test_signup_without_pass(self):
        data = {
            'user': self.USER_USERNAME2,
            'pass': ''
        }
        response = self.client.post(
            reverse('signup'),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 409)

    def test_signup_without_username(self):
        data = {
            'user': '',
            'pass': self.USER_PASSWORD2
        }
        response = self.client.post(
            reverse('signup'),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 409)

    def test_signup_useralready_exists(self):
        data = {
            'user': self.USER_USERNAME2,
            'pass': self.USER_PASSWORD2
        }
        response = self.client.post(
            reverse('signup'),
            data,
            format='json'
        )
        response = self.client.post(
            reverse('signup'),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 409)

    def test_signup_ok(self):
        data = {
            'user': self.USER_USERNAME2,
            'pass': self.USER_PASSWORD2
        }
        response = self.client.post(
            reverse('signup'),
            data,
            format='json'
        )

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
