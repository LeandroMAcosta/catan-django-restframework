from django.test import TestCase
from django.contrib.auth import authenticate
# from rest_framework.test import APIRequestFactory

from .models import User


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
