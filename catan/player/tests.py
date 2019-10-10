from django.contrib.auth import authenticate
from catan.tests import BaseTestCase
from player.models import Player
from game.models import Game


class PlayerTestCase(BaseTestCase):

    def test_authenticate_user(self):
        user = authenticate(
            username=self.USER_USERNAME,
            password=self.USER_PASSWORD
        )
        self.assertNotEqual(user, None)

    def test_create_player(self):
        user = authenticate(
            username=self.USER_USERNAME,
            password=self.USER_PASSWORD
        )
        self.i_game()
        games = Game.objects.all()
        game = games[0]
        self.i_player(user=user, game=game)
        player = Player.objects.get(user=user)

        self.assertNotEqual(player, None)
        self.assertEqual(Player.objects.count(), 1)
