from django.test import TestCase
from catan.tests import BaseTestCase
from game.models import Game, Hex, VertexPosition
from .views import HexListViewSets
# from django.contrib.auth import authenticate
# from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
# from .views import GameViewSets
# from .models import Game, VertexPosition, Hex
from .serializers import (
    GameSerializer,
    VertexPositionSerializer,
    HexSerializer
)


class BoardTestCase(TestCase):

    def SetUp(self):
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
        hexa = Hex.objects.create(game_id=game.id, position=vertex1.id,
                                  token=4, resource="lumber")
        self.assertEqual(hexa, None)
        self.assertEqual(hexa.game_id, game.id)
        self.assertEqual(hexa.position, vertex1.id)
        self.assertEqual(hexa.token, 4)
        self.assertEqual(hexa.resource, "lumber")
        Hex.objects.create(game_id=game.id, position=vertex2.id, token=9,
                           resource="wool")
        Hex.objects.create(game_id=game2.id, position=vertex1.id, token=12,
                           resource="nothing")
        self.assertEqual(Hex.objects.count(), 3)

        def HexListTest(self):
            view = HexListViewSets.as_view({'get': 'list'})
            factory = APIRequestFactory()
            url = 'api/games/'+str(gid)+'/board'
            request = factory.get(url)
            response = view(request)
            hexes = Hex.objects.filter(game_id=gid)
            serializer = HexSerializer(hexes, many=True)
            result = {'hexes': serializer.data}
            self.assertEqual(response.data, result)
