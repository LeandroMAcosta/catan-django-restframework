from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory

from card.models import Card
from resource.models import Resource
from player.models import Player

from .serializers import GameSerializer, HexSerializer
from .views import GameViewSets, HexListViewSets
from .models import Game, VertexPosition, Hex

User = get_user_model()


class ResourcesTestCase(TestCase):
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

    def test_list_cards_and_resources(self):
        factory = APIRequestFactory()
        request = factory.get('/api/games/<int:game_id>/player/')
        view = GameViewSets.as_view({'get': 'list_cards_and_resources'})

        user = User.objects.get(username=self.USER_USERNAME)
        game = Game.objects.get(pk=self.GAME_ID)
        player = Player.objects.get(game=game, user=user)

        force_authenticate(request, user=user)

        response = view(request, game_id=self.GAME_ID)

        cards = Card.objects.filter(player=player)
        resources = Resource.objects.filter(player=player)
        data = {
            'cards': cards,
            'resources': resources
        }

        serializer = GameSerializer(data)

        self.assertEqual(serializer.data, response.data)


class BoardTest(TestCase):

    def setUp(self):
        # Check if the game created right
        game = Game.objects.create()
        # Store this game_id for later use
        self.gid = game.id
        self.assertNotEqual(game, None)
        self.assertEqual(Game.objects.count(), 1)
        game2 = Game.objects.create()
        # Check if the vertex created right
        vertex1 = VertexPosition.objects.create(index=1, level=2)
        self.assertNotEqual(vertex1, None)
        self.assertEqual(vertex1.index, 1)
        self.assertEqual(vertex1.level, 2)
        vertex2 = VertexPosition.objects.create(index=1, level=1)
        self.assertEqual(VertexPosition.objects.count(), 2)
        # Make some hexes and check if the first got created properly
        hexa = Hex.objects.create(game_id=game, position=vertex1,
                                  token=4, resource="lumber")
        self.assertNotEqual(hexa, None)
        self.assertEqual(hexa.game_id, game)
        self.assertEqual(hexa.position, vertex1)
        self.assertEqual(hexa.token, 4)
        self.assertEqual(hexa.resource, "lumber")
        Hex.objects.create(game_id=game, position=vertex2, token=9,
                           resource="wool")
        Hex.objects.create(game_id=game2, position=vertex1, token=12,
                           resource="nothing")
        self.assertEqual(Hex.objects.count(), 3)

    def test_hex_list(self):
        view = HexListViewSets.as_view({'get': 'list'})
        factory = APIRequestFactory()
        gid = self.gid
        request = factory.get('api/games/<int:game_id>/board/')
        response = view(request, game_id=gid)
        hexes = Hex.objects.filter(game_id=gid)
        serializer = HexSerializer(hexes, many=True)
        result = {'hexes': serializer.data}
        self.assertEqual(response.data, result)
