from django.test import TestCase
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from .views import RoomsView
from .models import Room


factory = APIRequestFactory()
view = RoomsView.as_view()


class room_test(TestCase):
    def setUp(self):
        self.i_user('jorge', 'jorge@gmail.com', 'abcde1234')
        self.i_user('gon', 'gon@gmail.com', 'abcde1234')
        self.i_user('leandro', 'leandro@gmail.com', 'abcde1234')

        assert User.objects.count() == 3

    def test_room(self):
        new_room = Room.objects.create(
            name='room1',
            owner=User.objects.get(username='jorge')
        )
        new_room.save()
        # new_room.players.set(User.objects.get(username='gon'))

        assert Room.objects.count() == 1

    def test_list_room(self):
        # Make an authenticated request to the view...
        user = User.objects.get(username='jorge')
        request = factory.get('/api/room')
        force_authenticate(request, user=user)
        response = view(request)
        response.render()
        print(response.data)

    def test_join_room(self):
        pass

    def i_user(self, username, email, password):
        User.objects.create(
            username=username,
            email=email,
            password=password
        )
