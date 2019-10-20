from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny

from card.models import Card
from resource.models import Resource
from player.models import Player
from board.serializers import HexagonSerializer
from board.models import Hexagon

from .models import Game
from .serializers import GameSerializer


class HexListViewSets(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    def list(self, request, game):
        if Game.objects.filter(id=game).count() == 0:
            response = {'Error': 'Game does not exists'}
            return Response(
                response,
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        queryset = Hexagon.objects.filter(game=game)
        serializer = HexagonSerializer(queryset, many=True)
        size = queryset.count()
        if size == 0:
            return Response(
                {'Error': 'Empty Board'},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        elif size != 19:
            response = {
                'Error': 'Board incomplete',
                'Hexes': serializer.data
            }
            return Response(
                response,
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        return Response({'hexes': serializer.data}, status=status.HTTP_200_OK)


class GameViewSets(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GameSerializer
    queryset = Card.objects.all()

    def list_cards_and_resources(self, request, game):
        try:
            game = Game.objects.get(id=game)
            player = Player.objects.get(user=request.user, game=game)
            cards = Card.objects.filter(player=player)
            resources = Resource.objects.filter(player=player)
            data = {'cards': cards, 'resources': resources}
            serializer = self.serializer_class(data)

            return Response(serializer.data)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
