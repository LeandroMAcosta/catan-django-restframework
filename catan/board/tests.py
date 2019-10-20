from django.test import TestCase
from board.models import Board


class BoardTest(TestCase):
    def SetUp(self):
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

    # def test_create_board(self):
    #     board = Board.objects.create()

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
        # self.a*ssertEqual(h.game, g)
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

# Create your tests here.
