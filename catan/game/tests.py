from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory

from card.models import Card
from resource.models import Resource
from player.models import Player
from board.models import Vertex, Hexagon
from board.serializers import HexagonSerializer

from .serializers import GameSerializer
from .views import GameViewSets, HexListViewSets
from .models import Game

User = get_user_model()


class ResourcesTestCase(TestCase):
    def setUp(self):
        self.USER_USERNAME = "testuser"
        self.USER_EMAIL = "testuser@test.com"
        self.USER_PASSWORD = "supersecure"
        self.GAME = 666
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
            'id': self.GAME,
        }
        game = Game.objects.create(**game_data)
        game.save()

        # Create Player
        player_data = {
            'id': self.PLAYER_ID,
            'user': user,
            'game': game,
            'colour': 'colorcito',
        }
        player = Player.objects.create(**player_data)
        player.save()

    def test_list_cards_and_resources(self):
        factory = APIRequestFactory()
        request = factory.get('/api/games/<int:game>/player/')
        view = GameViewSets.as_view({'get': 'list_cards_and_resources'})

        user = User.objects.get(username=self.USER_USERNAME)
        game = Game.objects.get(pk=self.GAME)
        player = Player.objects.get(game=game, user=user)
        Card.objects.create(
            card_type='road_building',
            player=player
        )
        Card.objects.create(
            card_type='road_building',
            player=player
        )
        Resource.objects.create(
            resource='wool',
            player=player
        )

        force_authenticate(request, user=user)

        response = view(request, game=game.id)

        cards = Card.objects.filter(player=player)
        resources = Resource.objects.filter(player=player)

        data = {
            'cards': cards,
            'resources': resources
        }

        serializer = GameSerializer(data)

        self.assertEqual(serializer.data, response.data)


class GameTest(TestCase):

    def test_create_game(self):
        game = Game.objects.create()
        self.assertNotEqual(game, None)
