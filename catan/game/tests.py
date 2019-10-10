from django.test import TestCase
from game.models import Game, Hex, VertexPosition
from .views import HexListViewSets
from rest_framework.test import APIRequestFactory
from .serializers import (
    GameSerializer,
    VertexPositionSerializer,
    HexSerializer
)
# from django.contrib.auth import authenticate
# from rest_framework.test import force_authenticate
# from .views import GameViewSets
# from .models import Game, VertexPosition, Hex


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
        kwargs = {'game_id': gid}
        request = factory.get('api/games/<int:game_id>/board/')
        response = view(request, game_id=gid)
        hexes = Hex.objects.filter(game_id=gid)
        serializer = HexSerializer(hexes, many=True)
        result = {'hexes': serializer.data}
        self.assertEqual(response.data, result)
