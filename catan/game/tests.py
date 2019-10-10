from catan.tests import BaseTestCase
from django.contrib.auth import get_user_model

# from django.contrib.auth import authenticate
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from .views import GameViewSets
from .models import Game, VertexPosition, Hex
from card.models import Card
from resource.models import Resource
from .serializers import (
    GameSerializer,
    VertexPositionSerializer,
    HexSerializer
)
from card.serializers import CardSerializer
from resource.serializers import ResourceSerializer

User = get_user_model()


class ResourcesTestCase(BaseTestCase):

    def test_list_cards_and_resources(self):
        user = User.objects.get(username=self.USER_USERNAME)
        self.i_game()

        games = Game.objects.all()
        game = games[0]

        player = self.i_player(user=user, game=game)
        self.i_card(player)
        self.i_card(player)
        self.i_card(player)
        
        factory = APIRequestFactory()

        request = factory.get('/api/games/1/player/')

        view = GameViewSets.as_view({'get': 'list'})
        factory = APIRequestFactory()

        force_authenticate(request, user=user)

        print(view)
        
        response = view(request)

        # Get data from db
        cards = Card.objects.filter(player=player)
        resources = Resource.objects.filter(player=player)

        data = {
            'cards': CardSerializer(cards, many=True),
            'resources': ResourceSerializer(resources, many=True),
        }

        # serializer = RoomSerializer(rooms, many=True)

        print(data, response.data)
        # Compare the datadb with APIResponse
        # self.assertEqual(response.data, serializer.data)