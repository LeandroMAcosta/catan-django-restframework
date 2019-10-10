from django.test import TestCase
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
import json
from .views import RoomsView
from .models import Room


factory = APIRequestFactory()
view = RoomsView.as_view()


class room_test(TestCase):
    def setUp(self):
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

        assert User.objects.count() == 10

        new_room = Room.objects.create(
            name='room1',
            owner=User.objects.get(username='jorge')
        )
        new_room.players.set(User.objects.filter(username__contains='gon'))

        new_room = Room.objects.create(
            name='room2',
            owner=User.objects.get(username='leandro')
        )
        new_room.players.set(User.objects.filter(username__contains='lucas'))

        assert Room.objects.count() == 2

    def test_list_room(self):
        # Make an authenticated request to the view...
        user = User.objects.get(username='tester')
        request = factory.get('/api/room')
        force_authenticate(request, user=user)
        response = view(request)
        expected_answer = [
            {
                "id": 1, 
                "max_players": 4, 
                "name": "room1", 
                "owner": 2, 
                "players": ["gon", "gon1", "gon2", "gon3"]
            },
            {
                "id": 2,
                "max_players": 4,
                "name": "room2",
                "owner": 7,
                "players": ["lucas", "lucas1", "lucas2"]
            }
        ]
        assert json.dumps(response.data,sort_keys=True)==json.dumps(expected_answer,sort_keys=True)

    def test_join_room(self):
        user = User.objects.get(username='tester')
        
        request = factory.get('/api/room')
        force_authenticate(request, user=user)
        response = view(request)
        

    def i_user(self, username, email, password):
        User.objects.create(
            username=username,
            email=email,
            password=password
        )
