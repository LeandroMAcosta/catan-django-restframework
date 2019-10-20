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


class BoardTest(TestCase):

    def setUp(self):
        # Check if the game created right
        game = Game.objects.create()
        # Store this game for later use
        self.game = game
        # self.assertNotEqual(game, None)
        # self.assertEqual(Game.objects.count(), 1)
        # game2 = Game.objects.create()
        # # Check if the vertex created right
        # vertex1 = Vertex.objects.create(index=1, level=2)
        # self.assertNotEqual(vertex1, None)
        # self.assertEqual(vertex1.index, 1)
        # self.assertEqual(vertex1.level, 2)
        # vertex2 = Vertex.objects.create(index=1, level=1)
        # self.assertEqual(Vertex.objects.count(), 2)
        # # Make some hexes and check if the first got created properly
        # hexa = Hexagon.objects.create(game=game, position=vertex1,
        #                           token=4, resource="lumber")
        # self.assertNotEqual(hexa, None)
        # self.assertEqual(hexa.game, game)
        # self.assertEqual(hexa.position, vertex1)
        # self.assertEqual(hexa.token, 4)
        # self.assertEqual(hexa.resource, "lumber")
        # Hexagon.objects.create(game=game, position=vertex2, token=9,
        #                    resource="wool")
        # Hexagon.objects.create(game=game2, position=vertex1, token=12,
        #                    resource="nothing")
        # self.assertEqual(Hexagon.objects.count(), 3)

    def test_create_game(self):
        pass
        # game = Game.objects.create()
        # self.assertNotEqual(game, None)

    def test_create_vertex(self):
        pass
        # v = Vertex.objects.create(index=1, level=2)
        # self.assertNotEqual(v, None)
        # self.assertEqual(v.index, 1)
        # self.assertEqual(v.level, 2)

    def test_create_hex(self):
        pass
        # g = Game.objects.create()
        # v = Vertex.objects.create(level=0, index=0)
        # h = Hexagon.objects.create(game=g, position=v, token=2,
        #                        resource='brick')
        # self.assertNotEqual(h, None)
        # self.assertEqual(h.game, g)
        # self.assertEqual(h.position, v)
        # self.assertEqual(h.token, 2)
        # self.assertEqual(h.resource, 'brick')

    def test_hex_list(self):
        pass
        # gid = self.game.id
        # v = Vertex.objects.create(index=0, level=0)
        # h = Hexagon.objects.create(
        #     game=self.game,
        #     position=v, token=0,
        #                        resource="nothing")
        # # Create a full board
        # for i in range(0, 3):
        #     for j in range(0, 6*i):
        #         v = Vertex.objects.create(index=j, level=i)
        #         h = Hexagon.objects.create(game=self.game, position=v, token=0,
        #                                resource='lumber')
        # view = HexListViewSets.as_view({'get': 'list'})
        # factory = APIRequestFactory()
        # request = factory.get('api/games/<int:game>/board/')
        # response = view(request, game=gid)
        # hexes = Hexagon.objects.filter(game=gid)
        # serializer = HexagonSerializer(hexes, many=True)
        # result = {'hexes': serializer.data}
        # self.assertEqual(response.data, result)
