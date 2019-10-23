from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate
from rest_framework import status
from rest_framework.test import APIRequestFactory

from board.models import Board
from .serializers import RoomSerializer
from .views import RoomsView
from .models import Room
from . import functions_test as functions


class RoomTest(TestCase):
    def create_login_user(self, name, email, password):
        self.USER_USERNAME = name
        self.USER_EMAIL = email
        self.USER_PASSWORD = password
        # Create user
        user_data = {
            "username": self.USER_USERNAME,
            "email": self.USER_EMAIL,
            "password": self.USER_PASSWORD,
        }
        user = User._default_manager.create_user(**user_data)
        user.save()
        return user

    def create_board(self, name, user):
        board_data = {
            'name': name,
            'owner': user
        }
        board = Board(**board_data)
        board.save()
        return board

    def create_room(self, name, board, user, max_players, gs):
        room_data = {
            'name': name,
            'board': board,
            'max_players': max_players,
            'game_has_started': gs,
            'owner': user,
        }
        room = Room(**room_data)
        room.save()
        return room, room_data

    def setUp(self):
        user = self.create_login_user("pepe", "peep@gmail.com", "pepe123")

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

        board = self.create_board('boardcito', user)
        room, room_data = self.create_room('roomcito', board, user, 4, False)

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
        request = factory.put('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=user)
        view = RoomsView.as_view({'put': 'join'})
        response = view(request, pk=id)

        # Expected Output
        out = status.HTTP_406_NOT_ACCEPTABLE

        # Compare APIResponce with Expected Output
        self.assertEqual(response.status_code, out)

        # Test2: The user joins the room

        board = self.create_board('boardcito', user)
        room, _ = self.create_room('roomcito', board, user, 2, False)

        id = 1
        request = factory.put('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=user)
        view = RoomsView.as_view({'put': 'join'})
        response = view(request, pk=id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        room = Room.objects.get(id=1)
        data = {
            room
        }
        serializer = RoomSerializer(data, many=True).data
        self.assertEqual(serializer[0]['players'][0], 'pepe')

        # User already in the ROOM
        id = 1
        request = factory.put('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=user)
        view = RoomsView.as_view({'put': 'join'})
        response = view(request, pk=id)
        self.assertEqual(response.data, 'Already in the ROOM')

        # The ROOM is full
        # Filling the room
        user = self.create_login_user("u1", "u1@gmail.com", "supersecure")
        request = factory.put('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=user)
        view = RoomsView.as_view({'put': 'join'})
        response = view(request, pk=id)

        user = self.create_login_user("u2", "u2@gmail.com", "supersecure")
        request = factory.put('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=user)
        view = RoomsView.as_view({'put': 'join'})
        response = view(request, pk=id)

        self.assertEqual(response.data, 'The ROOM is full')

    def test_create_room(self):
        factory = APIRequestFactory()
        # Make an authenticated request to the view...
        user = User.objects.get(username=self.USER_USERNAME)

        # Test1: The Board not exist
        # APIResponse
        data = {
            'name': 'room',
            'board_id': 1
        }
        request = factory.post('/api/rooms/', data)
        force_authenticate(request, user=user)
        view = RoomsView.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.data, 'The Board not exist')

        # Test2: The ROOM already exists
        board = self.create_board('boardcito', user)
        room, room_data = self.create_room('roomcito', board, user, 2, False)

        data = {
            'name': 'roomcito',
            'board_id': 1
        }
        request = factory.post('/api/rooms/', data)
        force_authenticate(request, user=user)
        view = RoomsView.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.data, 'The room already exists')

        # Test3: Create ROOM
        board = self.create_board('boardcito', user)

        data = {
            'name': 'ROOMCREADA',
            'board_id': 2
        }
        request = factory.post('/api/rooms/', data)
        force_authenticate(request, user=user)
        view = RoomsView.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_start_game(self):
        factory = APIRequestFactory()
        # Make an authenticated request to the view...
        user = User.objects.get(username=self.USER_USERNAME)

        # Test1: The Room not exist
        # APIResponse
        id = 1
        request = factory.patch('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=user)
        view = RoomsView.as_view({'patch': 'start_game'})
        response = view(request, pk=1)
        # self.assertEqual(response.data, 'The ROOM does not exist')

        # Test2: The game has started
        board = self.create_board('boardcito', user)
        room, room_data = self.create_room('roomcito', board, user, 2, True)

        # APIResponse
        id = 1
        request = factory.patch('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=user)
        view = RoomsView.as_view({'patch': 'start_game'})
        response = view(request, pk=1)
        self.assertEqual(response.data, 'The game has started')

        # Test3: There are no 3 or 4 users to start playing
        room, room_data = self.create_room('lala', board, user, 4, False)

        # APIResponse
        id = 1
        request = factory.patch('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=user)
        view = RoomsView.as_view({'patch': 'start_game'})
        response = view(request, pk=2)
        self.assertEqual(response.data, '3 or 4 players are required')

        # Test4: The game is created correctly
        id = 2
        user = self.create_login_user("u1", "u1@gmail.com", "supersecure")
        request = factory.put('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=user)
        view = RoomsView.as_view({'put': 'join'})
        response = view(request, pk=id)

        self.create_login_user("u2", "u2@gmail.com", "supersecure")
        request = factory.put('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=user)
        view = RoomsView.as_view({'put': 'join'})
        response = view(request, pk=id)

        self.create_login_user("u3", "u3@gmail.com", "supersecure")
        request = factory.put('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=user)
        view = RoomsView.as_view({'put': 'join'})
        response = view(request, pk=id)

        # APIResponse
        request = factory.patch('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=user)
        view = RoomsView.as_view({'patch': 'start_game'})
        response = view(request, pk=id)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_cancel_lobby(self):
        pass
        # La room no existe
        # La room se elimina (cancela) correctamente
