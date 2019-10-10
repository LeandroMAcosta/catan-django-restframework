from django.test import TestCase
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from .views import RoomsView
from .models import Room
from .serializers import RoomSerializer


class RoomTest(TestCase):

    def i_user(self, username, email, password):
        User.objects.create(
            username=username,
            email=email,
            password=password
        )

    def i_room(self, name, owner, players):
        new_room = Room.objects.create(
            name=name,
            owner=User.objects.get(username=owner)
        )
        new_room.players.set(User.objects.filter(username__contains=players))

    def setUp(self):
        self.view = RoomsView.as_view({'get': 'list'})
        self.factory = APIRequestFactory()

        self.i_user('tester', 'tester@gmail.com', 'abcde1234')
        self.i_user('jorge', 'jorge@gmail.com', 'abcde1234')
        self.i_user('gon', 'gon@gmail.com', 'abcde1234')
        self.i_user('gon1', 'gon1@gmail.com', 'abcde1234')
        self.i_user('gon2', 'gon2@gmail.com', 'abcde1234')
        self.i_user('gon3', 'gon3@gmail.com', 'abcde1234')
        self.i_user('leandro', 'leandro@gmail.com', 'abcde1234')
        self.i_user('lucas', 'lucas@gmail.com', 'abcde1234')
        self.i_user('lucas1', 'lucas1@gmail.com', 'abcde1234')
        self.i_user('lucas2', 'lucas2@gmail.com', 'abcde1234')

        self.assertEqual(User.objects.count(), 10)

        self.i_room('room1', 'jorge', 'gon')
        self.i_room('room2', 'leandro', 'lucas')

        self.assertEqual(Room.objects.count(), 2)

    def test_list_room(self):
        # Make an authenticated request to the view...
        user = User.objects.get(username='tester')
        request = self.factory.get('/api/room')
        force_authenticate(request, user=user)
        response = self.view(request)

        # Get data from db
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
        # Compare the datadb with APIResponse
        self.assertEqual(response.data, serializer.data)

    def test_join_room(self):
        pass
<<<<<<< Updated upstream
=======

        """factory = APIRequestFactory()
        user = User.objects.get(username='gon')
        request = factory.put('/api/users/login/', username=user, password='abcde1234')

        print(request)"""
>>>>>>> Stashed changes
