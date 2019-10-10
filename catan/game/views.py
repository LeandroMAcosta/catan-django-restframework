from rest_framework.response import Response
from rest_framework import permissions, viewsets, status
from .models import Hex, Game
from .serializers import HexSerializer
from game.serializers import GameSerializer
from card.models import Card
from resource.models import Resource
from player.models import Player


class HexListViewSets(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)

    def list(self, request, game_id):
        queryset = Hex.objects.filter(game_id=game_id)
        serializer = HexSerializer(queryset, many=True)
        return Response({'hexes': serializer.data})


class GameViewSets(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GameSerializer
    queryset = Card.objects.all()

    def list_cards_and_resources(self, request, game_id):
        try:
            game = Game.objects.get(id=game_id)
            player = Player.objects.get(user=request.user, game=game)

            cards = Card.objects.filter(player=player)
            resources = Resource.objects.filter(player=player)
            data = {
                'cards': cards,
                'resources': resources
            }
            serializer = self.serializer_class(data)

            return Response(serializer.data)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
