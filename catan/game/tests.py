from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import (
    force_authenticate,
    APIRequestFactory,
    APITestCase
)

from card.models import Card
from resource.models import Resource
from player.models import Player
from board.models import Board
from lobby.models import Room

from .serializers import GameSerializer
from .views import GameViewSets
from .models import Game

User = get_user_model()


class ResourcesTestCase(TestCase):
    def setUp(self):
        self.USER_USERNAME = "testuser2"
        self.USER_EMAIL = "testuser2@test.com"
        self.USER_PASSWORD = "supersecure"
        self.GAME = 6667
        self.PLAYER_ID = 6677

        # Create user
        user_data = {
            "username": self.USER_USERNAME,
            "email": self.USER_EMAIL,
            "password": self.USER_PASSWORD,
        }
        user = User._default_manager.create_user(**user_data)
        user.save()

        board_data = {
            'name': 'boardcito',
            'owner': user
        }
        board = Board(**board_data)
        board.save()

        room_data = {
            'name': 'roomcito',
            'board': board,
            'game_has_started': False,
            'owner': user,
        }
        room = Room(**room_data)
        room.save()

        game = Game(room=room)
        game.save()

        self.GAME = game.id
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


class GameTest(APITestCase):
    def setUp(self):
        # User
        self.username = "testuser2"
        self.email = "testuser2@test.com"
        self.password = "supersecure"
        self.user = User._default_manager.create_user(
            username=self.username,
            email=self.email,
        )
        self.user.set_password(self.password)
        self.user.save()

        # Board
        self.board_name = 'boardcito'
        self.board_owner = self.user
        self.board = Board(
            name=self.board_name,
            owner=self.board_owner
        )
        self.board.save()

        # Room
        self.room = Room(
            name='roomcito',
            board=self.board,
            game_has_started=True,
            owner=self.user,
        )
        self.room.save()

        # Game
        self.game = Game(room=self.room)
        self.game.save()

        # Player
        self.player = Player(
            user=self.user,
            game=self.game,
            colour='colorcito'
        )
        self.player.save()
        self.client.force_authenticate(self.user)

    def test_game_bad_request(self):
        data = {
            'type': 'build_settlement',
            'payload': {
                'index': 0,
                'level': 0
            }
        }

        needed_resources = [('brick', 1), ('lumber', 1),
                            ('grain', 1), ('wool', 1)]

        self.player.increase_resources(needed_resources)

        response = self.client.post(
            reverse('player-action', args=[self.game.id+10000]),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 404)

    def test_game_bad_action(self):
        data = {
            'type': 'bad_action',
            'payload': {
                'index': 0,
                'level': 0
            }
        }

        needed_resources = [('brick', 1), ('lumber', 1),
                            ('grain', 1), ('wool', 1)]

        self.player.increase_resources(needed_resources)

        response = self.client.post(
            reverse('player-action', args=[self.game.id]),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, "Wrong action.")

    def test_settlement_ok(self):
        data = {
            'type': 'build_settlement',
            'payload': {
                'index': 0,
                'level': 0
            }
        }

        needed_resources = [('brick', 1), ('lumber', 1),
                            ('grain', 1), ('wool', 1)]

        self.player.increase_resources(needed_resources)

        response = self.client.post(
            reverse('player-action', args=[self.game.id]),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_settlement_few_resources(self):
        data = {
            'type': 'build_settlement',
            'payload': {
                'index': 0,
                'level': 0
            }
        }

        needed_resources = [('lumber', 1), ('grain', 1), ('wool', 1)]

        self.player.increase_resources(needed_resources)

        response = self.client.post(
            reverse('player-action', args=[self.game.id]),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Not enough resources")

    def test_settlement_out_of_bounds(self):
        data = {
            'type': 'build_settlement',
            'payload': {
                'index': 10,
                'level': 10
            }
        }

        response = self.client.post(
            reverse('player-action', args=[self.game.id]),
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_settlement_game_not_exits(self):
        data = {
            'type': 'build_settlement',
            'payload': {
                'index': 0,
                'level': 0
            }
        }

        response = self.client.post(
            reverse('player-action', args=[30]),
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_road_ok(self):

        resources = [('brick', 1), ('lumber', 1)]
        self.player.increase_resources(resources)
        data = {
            'type': 'build_road',
            'payload': [
                {
                    'level': 0,
                    'index': 0
                },
                {
                    'level': 0,
                    'index': 1,
                }

            ]
        }

        response = self.client.post(
            reverse('player-action', args=[self.game.id]),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_road_oob(self):
        data = {
            'type': 'build_road',
            'payload': [
                {
                    'level': 10,
                    'index': 20
                },
                {
                    'level': 42,
                    'index': 69,
                }

            ]
        }

        response = self.client.post(
            reverse('player-action', args=[self.game.id]),
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_road_non_adjacent(self):
        data = {
            'type': 'build_road',
            'payload': [
                {
                    'level': 0,
                    'index': 0
                },
                {
                    'level': 2,
                    'index': 0,
                }

            ]
        }

        response = self.client.post(
            reverse('player-action', args=[self.game.id]),
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_road_repeated_arguments(self):
        data = {
            'type': 'build_road',
            'payload': [
                {
                    'level': 0,
                    'index': 0
                },
                {
                    'level': 0,
                    'index': 0,
                }

            ]
        }

        response = self.client.post(
            reverse('player-action', args=[self.game.id]),
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_road_insufficient_arguments(self):
        data = {
            'type': 'build_road',
            'payload': [
                {
                    'level': 0,
                    'index': 0
                }

            ]
        }

        response = self.client.post(
            reverse('player-action', args=[self.game.id]),
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_road_too_many_arguments(self):
        data = {
            'type': 'build_road',
            'payload': [
                {
                    'level': 0,
                    'index': 0
                },
                {
                    'level': 0,
                    'index': 1,
                },
                {
                    'level': 0,
                    'index': 2
                },

            ]
        }

        response = self.client.post(
            reverse('player-action', args=[self.game.id]),
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_road_used_edge(self):
        data = {
            'type': 'build_road',
            'payload': [
                {
                    'level': 0,
                    'index': 0
                },
                {
                    'level': 0,
                    'index': 1,
                }

            ]
        }
        response = self.client.post(
            reverse('player-action', args=[self.game.id]),
            data,
            format='json'
        )

        # Second road SHOULD FAIL

        response = self.client.post(
            reverse('player-action', args=[self.game.id]),
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_buy_card(self):

        resources = [('wool', 1), ('ore', 1), ('grain', 1)]
        self.player.increase_resources(resources)
        data = {
            'type': 'buy_card',
            'payload': None
        }
        response = self.client.post(
            reverse('player-action', args=[self.game.id]),
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_buy_card_no_resources(self):
        data = {
            'type': 'buy_card',
            'payload': None
        }
        response = self.client.post(
            reverse('player-action', args=[self.game.id]),
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_bank_trade_ok(self):
        data = {
            'type': 'bank_trade',
            'payload': {
                'give': 'wool',
                'receive': 'grain'
            }
        }
        give = self.player.get_resource('wool')
        give.amount = 4
        give.save()

        response = self.client.post(
            reverse('player-action', args=[self.game.id]),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Trade done.")

    def test_bank_trade_equal_receive_and_give(self):
        data = {
            'type': 'bank_trade',
            'payload': {
                'give': 'wool',
                'receive': 'wool'
            }
        }
        response = self.client.post(
            reverse('player-action', args=[self.game.id]),
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Resources must be different.")

    def test_bank_trade_bad_receive(self):
        data = {
            'type': 'bank_trade',
            'payload': {
                'give': 'wool',
                'receive': 'badreceive'
            }
        }
        response = self.client.post(
            reverse('player-action', args=[self.game.id]),
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Resource not exists.")

    def test_bank_trade_few_resources(self):
        data = {
            'type': 'bank_trade',
            'payload': {
                'give': 'wool',
                'receive': 'grain'
            }
        }
        give = self.player.get_resource('wool')
        give.amount = 3
        give.save()

        response = self.client.post(
            reverse('player-action', args=[self.game.id]),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Insufficient resources.")
