from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status

from board.serializers import HexagonSerializer
from resource.models import Resource
from player.models import Player
from card.models import Card

from .serializers import GameSerializer
from .models import Game


class GameViewSets(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GameSerializer
    queryset = Game.objects.all()

    def list(self, request, pk):
        game = self.get_object()
        board = game.get_board()
        hexagons = board.hexagon_set.all()
        serializer = HexagonSerializer(hexagons, many=True)
        size = hexagons.count()
        if size == 0:
            return Response(
                {'Error': 'Empty Board'},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({'hexes': serializer.data})

    def list_cards_and_resources(self, request, pk):
        game = self.get_object()
        player = get_object_or_404(Player, user=request.user, game=game)
        cards = Card.objects.filter(player=player)
        resources = Resource.objects.filter(player=player)
        data = {'cards': cards, 'resources': resources}
        serializer = self.serializer_class(data)

        return Response(serializer.data)

    def action(self, request, pk):
        try:
            if not Game.objects.filter(pk=pk).exists():
                raise Exception("Game does not exist")
            game = self.get_object()
            player = Player.objects.get(game=game, user=request.user)
            data = request.data['payload']
            action = request.data['type']
            if action not in player.available_actions():
                raise Exception("Wrong action.")
            message, response_status = getattr(player, action)(data)
            return Response(
                message,
                status=response_status
            )
        except AttributeError:
            return Response(
                "Bad Request",
                status=status.HTTP_400_BAD_REQUEST
            )
        except Player.DoesNotExist:
            return Response(
                "Player of authenticated user does not exist",
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as error:
            err = str(error)
            return Response(
                err,
                status=status.HTTP_404_NOT_FOUND
            )
