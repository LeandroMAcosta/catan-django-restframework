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
        self.user = self.create_login_user("pepe", "peep@gmail.com", "pepe123")
        self.factory = APIRequestFactory()

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
        board.hexagon_set.create()
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

    def test_list_room_without_rooms(self):
        # Make an authenticated request to the view...
        # APIResponse
        request = self.factory.get('/api/rooms/')
        force_authenticate(request, user=self.user)
        view = RoomsView.as_view({'get': 'list_rooms'})
        response = view(request)

        # Expected serializer output
        data = []
        serializer = RoomSerializer(data, many=True)

        self.assertEqual(response.data, serializer.data, [])

    def test_list_rooms_ok(self):
        board = self.create_board('boardcito', self.user)
        room, room_data = self.create_room(
            'roomcito',
            board,
            self.user,
            4,
            False
        )

        # APIResponse
        request = self.factory.get('/api/rooms/')
        force_authenticate(request, user=self.user)
        view = RoomsView.as_view({'get': 'list_rooms'})
        response = view(request)
        assert response.status_code == 200

        # Expected serializer output
        room = Room.objects.get(name='roomcito')
        data = {
            room
        }
        serializer = RoomSerializer(data, many=True)

        self.assertEqual(response.data, serializer.data, room_data)

    def test_list_room_does_not_exists(self):
        # APIResponse
        id = 123456789
        request = self.factory.get('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=self.user)
        view = RoomsView.as_view({'get': 'list_room'})
        response = view(request, pk=id)
        assert response.status_code == 406
        self.assertEqual(response.data, 'The ROOM does not exist')

    def test_list_room_ok(self):
        board = self.create_board('boardcito', self.user)
        room, room_data = self.create_room(
            'roomcito',
            board,
            self.user,
            4,
            False
        )
        board2 = self.create_board('boardcito2', self.user)
        room2, room_data2 = self.create_room(
            'roomcito2',
            board,
            self.user,
            4,
            False
        )

        # APIResponse
        id = 1
        request = self.factory.get('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=self.user)
        view = RoomsView.as_view({'get': 'list_room'})
        response = view(request, pk=id)
        assert response.status_code == 200
        self.assertEqual(response.data['id'], id)

        id = 2
        request = self.factory.get('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=self.user)
        view = RoomsView.as_view({'get': 'list_room'})
        response = view(request, pk=id)
        assert response.status_code == 200
        self.assertEqual(response.data['id'], id)

    def test_join_room_does_not_exists(self):
        id = 123456789
        request = self.factory.put('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=self.user)
        view = RoomsView.as_view({'put': 'join'})
        response = view(request, pk=id)

        # Compare APIResponce with Expected Output
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_join_ok(self):
        board = self.create_board('boardcito', self.user)
        room, _ = self.create_room(
            'roomcito',
            board,
            self.user,
            2,
            False
        )

        id = 1
        request = self.factory.put('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=self.user)
        view = RoomsView.as_view({'put': 'join'})
        response = view(request, pk=id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        room = Room.objects.get(id=1)
        data = {
            room
        }
        serializer = RoomSerializer(data, many=True).data
        self.assertEqual(serializer[0]['players'][0], 'pepe')

        return board, room

    def test_join_user_alredy_in_room(self):
        boar, room = self.test_join_ok()
        id = 1
        request = self.factory.put('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=self.user)
        view = RoomsView.as_view({'put': 'join'})
        response = view(request, pk=id)
        self.assertEqual(response.data, 'Already in the ROOM')

    def test_join_room_full(self):
        boar, room = self.test_join_ok()

        # Filling the room
        id = 1
        user = self.create_login_user("u1", "u1@gmail.com", "supersecure")
        request = self.factory.put('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=user)
        view = RoomsView.as_view({'put': 'join'})
        response = view(request, pk=id)

        user = self.create_login_user("u2", "u2@gmail.com", "supersecure")
        request = self.factory.put('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=user)
        view = RoomsView.as_view({'put': 'join'})
        response = view(request, pk=id)

        self.assertEqual(response.data, 'The ROOM is full')

    def test_create_room_Board_not_exist(self):
        # APIResponse
        data = {
            'name': 'room',
            'board_id': 1
        }
        request = self.factory.post('/api/rooms/', data)
        force_authenticate(request, user=self.user)
        view = RoomsView.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.data, 'The Board not exist')

    def test_create_room_Room_already_exists(self):
        board = self.create_board('boardcito', self.user)
        room, room_data = self.create_room(
            'roomcito',
            board,
            self.user,
            2,
            False
        )

        data = {
            'name': 'roomcito',
            'board_id': board.id
        }
        request = self.factory.post('/api/rooms/', data)
        force_authenticate(request, user=self.user)
        view = RoomsView.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.data, 'The room already exists')

    def test_create_room_ok(self):
        board = self.create_board('boardcito', self.user)

        data = {
            'name': 'ROOMCREADA',
            'board_id': board.id
        }
        request = self.factory.post('/api/rooms/', data)
        force_authenticate(request, user=self.user)
        view = RoomsView.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_start_game_room_not_exist(self):
        # APIResponse
        id = 1
        request = self.factory.patch('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=self.user)
        view = RoomsView.as_view({'patch': 'start_game'})
        response = view(request, pk=1)
        self.assertEqual(response.data, 'The ROOM does not exist')

    def test_start_game_has_started(self):
        board = self.create_board('boardcito', self.user)
        room, room_data = self.create_room(
            'roomcito',
            board,
            self.user,
            2,
            True
        )

        # APIResponse
        id = 1
        request = self.factory.patch('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=self.user)
        view = RoomsView.as_view({'patch': 'start_game'})
        response = view(request, pk=1)
        self.assertEqual(response.data, 'The game has started')

    def test_start_game_3or4_players(self):
        board = self.create_board('boardcito', self.user)
        room, room_data = self.create_room('lala', board, self.user, 4, False)

        # APIResponse
        id = 1
        request = self.factory.patch('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=self.user)
        view = RoomsView.as_view({'patch': 'start_game'})
        response = view(request, pk=id)
        self.assertEqual(response.data, '3 or 4 players are required')

    def test_start_game_ok(self):
        board = self.create_board('boardcito', self.user)
        room, room_data = self.create_room('lala', board, self.user, 4, False)

        id = 1
        user = self.create_login_user("u1", "u1@gmail.com", "supersecure")
        request = self.factory.put('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=user)
        view = RoomsView.as_view({'put': 'join'})
        response = view(request, pk=id)

        user = self.create_login_user("u2", "u2@gmail.com", "supersecure")
        request = self.factory.put('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=user)
        view = RoomsView.as_view({'put': 'join'})
        response = view(request, pk=id)

        user = self.create_login_user("u3", "u3@gmail.com", "supersecure")
        request = self.factory.put('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=user)
        view = RoomsView.as_view({'put': 'join'})
        response = view(request, pk=id)

        # APIResponse
        request = self.factory.patch('/api/rooms/' + str(id) + '/')
        force_authenticate(request, user=user)
        view = RoomsView.as_view({'patch': 'start_game'})
        response = view(request, pk=id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cancel_lobby(self):
        pass
        # La room no existe
        # La room se elimina (cancela) correctamente
