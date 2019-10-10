from django.test import TestCase
from django.contrib.auth import get_user_model

from player.models import Player
from card.models import Card
from lobby.models import Room
from game.models import Game


User = get_user_model()


class BaseTestCase(TestCase):
    def setUp(self):
        self._API_BASE = 'http://127.0.0.1:8000/api/'
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
        self.assertEqual(User.objects.count(), 1)

    def i_user(self, username, email, password):
        return User.objects.create(
            username=username,
            email=email,
            password=password
        )

    def i_player(self, user, game, colour='rojito'):
        return Player.objects.create(
            user=user,
            colour=colour,
            game=game
        )

    def i_card(self, player, card_type='road_building'):
        return Card.objects.create(
            player=player,
            card_type=card_type,
        )

    def i_room(self, name, owner, players):
        new_room = Room.objects.create(
            name=name,
            owner=User.objects.get(username=owner)
        )
        new_room.players.set(User.objects.filter(username__contains=players))

    def i_game(self):
        Game.objects.create()
