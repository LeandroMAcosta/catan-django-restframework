from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory

from game.models import Game
from game.views import HexListViewSets
from lobby.models import Room

from .models import Board, Hexagon
from .serializers import HexagonSerializer

User = get_user_model()


class BoardTest(TestCase):
    def setUp(self):
        # Create user
        user_data = {
            "username": "testuser",
            "email": "testuser@test.com",
            "password": "supersecure",
        }
        self.user = User._default_manager.create_user(**user_data)
        self.user.save()
        board_data = {
            'name': 'boardcito',
            'owner': self.user
        }
        self.board = Board(**board_data)
        self.board.save()

        room_data = {
            'name': 'roomcito',
            'board': self.board,
            'game_has_started': False,
            'owner': self.user,
        }
        self.room = Room(**room_data)
        self.room.save()
        self.game = Game(room=self.room)
        self.game.save()

    def test_create_board(self):
        board = Board.objects.create(owner=self.user, name="TestBoard")
        board.save()
        self.assertNotEqual(board, None)
        self.assertEqual(board.owner, self.user)
        self.assertEqual(board.name, "TestBoard")

    def test_create_hex(self):
        b = Board.objects.create(owner=self.user, name="Placeholder")
        h = Hexagon.objects.create(board=b, level=1, index=2, token=2,
                                   resource='brick')
        h.save()
        self.assertNotEqual(h, None)
        self.assertEqual(h.board, b)
        self.assertEqual(h.level, 1)
        self.assertEqual(h.index, 2)
        self.assertEqual(h.token, 2)
        self.assertEqual(h.resource, 'brick')

    def test_hex_list(self):
        hexagon = Hexagon.objects.create(
            board=self.board,
            level=0,
            index=0,
            token=1,
            resource="wool"
        )
        hexagon.save()

        view = HexListViewSets.as_view({'get': 'list'})
        factory = APIRequestFactory()
        request = factory.get('api/games/<int:game>/board/')
        response = view(request, game=self.game.id)
        hexes = self.board.hexagon_set.all()
        serializer = HexagonSerializer(hexes, many=True)
        result = {'hexes': serializer.data}
        self.assertEqual(response.data, result)
