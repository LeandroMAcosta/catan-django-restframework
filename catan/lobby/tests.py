from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory

from catan.tests import BaseTestCase

from .views import RoomsView
from .models import Room
from .serializers import RoomSerializer


class RoomTest(TestCase):

    def setUp(self):

        BaseTestCase.i_user(self, 'tester', 'tester@gmail.com', 'abcde1234')
        BaseTestCase.i_user(self, 'jorge', 'jorge@gmail.com', 'abcde1234')
        BaseTestCase.i_user(self, 'gon', 'gon@gmail.com', 'abcde1234')
        BaseTestCase.i_user(self, 'gon1', 'gon1@gmail.com', 'abcde1234')
        BaseTestCase.i_user(self, 'gon2', 'gon2@gmail.com', 'abcde1234')
        BaseTestCase.i_user(self, 'gon3', 'gon3@gmail.com', 'abcde1234')
        BaseTestCase.i_user(self, 'leandro', 'leandro@gmail.com', 'abcde1234')
        BaseTestCase.i_user(self, 'lucas', 'lucas@gmail.com', 'abcde1234')
        BaseTestCase.i_user(self, 'lucas1', 'lucas1@gmail.com', 'abcde1234')
        BaseTestCase.i_user(self, 'lucas2', 'lucas2@gmail.com', 'abcde1234')

        self.assertEqual(User.objects.count(), 10)

        BaseTestCase.i_room(self, 'room1', 'jorge', 'gon')
        BaseTestCase.i_room(self, 'room2', 'leandro', 'lucas')

        self.assertEqual(Room.objects.count(), 2)

    def test_list_room(self):
        view = RoomsView.as_view({'get': 'list'})
        factory = APIRequestFactory()

        # Make an authenticated request to the view...
        user = User.objects.get(username='tester')
        request = factory.get('/api/rooms')
        force_authenticate(request, user=user)
        response = view(request)

        # Get data from db
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)

        # Compare the datadb with APIResponse
        self.assertEqual(response.data, serializer.data)

    def test_join_room(self):
        pass
        # Que se una a una room correctamente
        # Que ya este en una room
        # Que la room no exista
        # Que la room este llena

    def test_create_room(self):
        pass
        # Que se cree una room correctamente
        # Campos vacios: tipo "name": o "board_id":
        # Rooms que ya existen
        # Nombres de Room que ya existen