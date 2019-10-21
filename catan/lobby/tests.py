from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate
from rest_framework import status
from rest_framework.test import APIRequestFactory

from board.models import Board
from .serializers import RoomSerializer
from .views import RoomsView
from .models import Room


class RoomTest(TestCase):

    def setUp(self):
        self.USER_USERNAME = "testuser"
        self.USER_EMAIL = "testuser@test.com"
        self.USER_PASSWORD = "supersecure"

        self.USER_USERNAME = "testuser2"
        self.USER_EMAIL = "testuser2@test.com"
        self.USER_PASSWORD = "supersecure"

        # Create user
        user_data = {
            "username": self.USER_USERNAME,
            "email": self.USER_EMAIL,
            "password": self.USER_PASSWORD,
        }
        user = User._default_manager.create_user(**user_data)
        user.save()

    def test_list_room(self):
        factory = APIRequestFactory()
        # Make an authenticated request to the view...
        user = User.objects.get(username=self.USER_USERNAME)

        # Test1: WITHOUT rooms

        # APIResponse
        request = factory.get('/api/rooms/')
        force_authenticate(request, user=user)
        view = RoomsView.as_view({'get': 'list'})
        response = view(request)

        # Expected serializer output
        data = []
        serializer = RoomSerializer(data, many=True)

        self.assertEqual(response.data, serializer.data, [])

        # Test2: WHIT rooms

        # Create board
        board_data = {
            'name': 'boardcito',
            'owner': user
        }
        board = Board(**board_data)
        board.save()

        # Create rooms
        room_data = {
            'name': 'roomcito',
            'board': board,
            'game_has_started': False,
            'owner': user,
        }
        room = Room(**room_data)
        room.save()

        # APIResponse
        request = factory.get('/api/rooms/')
        force_authenticate(request, user=user)
        view = RoomsView.as_view({'get': 'list'})
        response = view(request)
        assert response.status_code == 200

        # Expected serializer output
        room = Room.objects.get(name='roomcito')
        data = {
            room
        }
        serializer = RoomSerializer(data, many=True)

        self.assertEqual(response.data, serializer.data, room_data)

    def test_join_room(self):
        factory = APIRequestFactory()
        # Make an authenticated request to the view...
        user = User.objects.get(username=self.USER_USERNAME)

        # Test1: The Room does not exist
        # APIResponse
        id = 123456789
        request = factory.put('/api/rooms/' + str(id))
        force_authenticate(request, user=user)
        view = RoomsView.as_view({'put': 'join'})
        response = view(request, room_id=id)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        # Que se una a una room correctamente
        # Que ya este en esa room
        # Que la room este llena

    def test_create_room(self):
        pass
        # Que se cree una room correctamente
        # Campos vacios: tipo "name": o "board_id": (datos incorrectos)
        # Rooms que ya existen
        # Nombres de Room que ya se estan usando
        # No existe la Board

    def test_start_game(self):
        pass
        # El juego se crea correctamente
        # El juego ya habia empezado
        # No hay 3 o 4 usuarios para empezar a jugar
        # La room no existe

    def test_cancel_lobby(self):
        pass
        # La room no existe
        # La room se elimina (cancela) correctamente
