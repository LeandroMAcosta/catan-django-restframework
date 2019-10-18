from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny

from card.models import Card
from resource.models import Resource
from player.models import Player

from .models import Hex, Game
from .serializers import HexSerializer, GameSerializer


class HexListViewSets(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    def list(self, request, game_id):
        if Game.objects.filter(id=game_id).count() == 0:
            return Response({'Error': 'Game does not exists'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        queryset = Hex.objects.filter(game_id=game_id)
        serializer = HexSerializer(queryset, many=True)
        size = queryset.count()
        if size == 0:
            return Response({'Error': 'Empty Board'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        elif size != 19:
            return Response({'Error': 'Board incomplete',
                             'Hexes': serializer.data},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'hexes': serializer.data}, status=status.HTTP_200_OK)


class GameViewSets(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GameSerializer
    queryset = Card.objects.all()

    def list_cards_and_resources(self, request, game_id):
        try:
            game = Game.objects.get(id=game_id)
            player = Player.objects.get(user=request.user, game=game)
            cards = Card.objects.filter(player=player)
            resources = Resource.objects.filter(player=player)
            data = {'cards': cards, 'resources': resources}
            serializer = self.serializer_class(data)

            return Response(serializer.data)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
