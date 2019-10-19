from django.test import TestCase
from django.contrib.auth import authenticate, get_user_model

from game.models import Game

from .models import Player

User = get_user_model()


class PlayerTestCase(TestCase):
    def setUp(self):
        self.USER_USERNAME = "testuser"
        self.USER_EMAIL = "testuser@test.com"
        self.USER_PASSWORD = "supersecure"
        self.GAME_ID = 666
        self.PLAYER_ID = 667

        # Create user
        user_data = {
            "username": self.USER_USERNAME,
            "email": self.USER_EMAIL,
            "password": self.USER_PASSWORD,
        }
        user = User._default_manager.create_user(**user_data)
        user.save()

        # Create Game
        game_data = {
            'id': self.GAME_ID,
        }
        game = Game.objects.create(**game_data)
        game.save()

        # Create Player
        player_data = {
            'id': self.PLAYER_ID,
            'user': user,
            'game': game,
            'colour': 'colour',
        }
        player = Player.objects.create(**player_data)
        player.save()
