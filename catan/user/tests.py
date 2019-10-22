from django.test import TestCase
from django.contrib.auth import authenticate
from rest_framework.test import APIRequestFactory
# from django.urls import reverse

from .models import User
from .serializers import UserSerializer
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
        
    def test_correct_signup(self):
        """
        url = /api/users/
        method = POST
        data = user y pass
        """
        data = {
            'username': 'testuser2',
            'email': 'foobar@example.com',
            'password': 'somepassword'
        }
        factory = APIRequestFactory()
        view = UserSignup.as_view({'post': 'create'})
        request = factory.post('/api/users/', data=data, format='json')
        response = view(request)
        serializer = UserSerializer(data)
        
        self.assertEqual(data, serializer.data)
        self.assertEqual(response.status_code, 201)
        
        print(response.status_code)

    def test_passwordempty_signup(self):
        """
        url = /api/users/
        method = POST
        data = user y pass
        """
        data = {
            'username': 'testuser2',
            'email': 'foobar@example.com',
            'password': ''
        }
        factory = APIRequestFactory()
        view = UserSignup.as_view({'post': 'create'})
        request = factory.post('/api/users/signup/', data=data, format='json')
        response = view(request)
        serializer = UserSerializer(data)
        
        self.assertEqual(data, serializer.data)
        self.assertEqual(response.status_code, 409)
        
        print(response.status_code)
        
    def test_usernameempty_signup(self):
        """
        url = /api/users/
        method = POST
        data = user y pass
        """
        data = {
            'username': '',
            'email': 'some@example.com',
            'password': 'somepassword'
        }
        factory = APIRequestFactory()
        request = factory.post('/api/users/signup/', data=data, format='json')
        view = UserSignup.as_view({'post': 'create'})
        response = view(request)
        serializer = UserSerializer(data)
        
        self.assertEqual(data, serializer.data)
        self.assertEqual(response.status_code, 409)
       
        print(response.status_code)

    def test_username_alredyexist(self):
        """
        url = /api/users/
        method = POST
        data = user y pass
        """
        data = {
            'username': 'testuser',
            'email': 'foobar@example.com',
            'password': 'somepassword'
        }

        view = UserSignup.as_view({'post': 'create'})
        factory = APIRequestFactory()
        request = factory.post('/api/users/signup/', data=data, format='json')
        response = view(request)
        serializer = UserSerializer(data)
       
        self.assertEqual(data, serializer.data)
        self.assertEqual(response.status_code, 409)
        
        print(response.status_code)

    def test_email_alredyexist(self):
        """
        url = /api/users/
        method = POST
        data = user y pass
        """
        data = {
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password': 'somepassword'
        }

        view = UserSignup.as_view({'post': 'create'})
        factory = APIRequestFactory()
        request = factory.post('/api/users/signup/', data=data, format='json')
        response = view(request)
        serializer = UserSerializer(data)
       
        self.assertEqual(data, serializer.data)
        self.assertEqual(response.status_code, 409)
        
        print(response.status_code)