from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, status

from board.serializers import HexagonSerializer
from board.models import Hexagon, Vertex
from resource.models import Resource
from player.models import Player
from card.models import Card

from .serializers import GameSerializer
from .models import Game


class HexListViewSets(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    def list(self, request, game):

        if not Game.objects.filter(id=game).exist():
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
                status=status.HTTP_404_NOT_FOUND
            )
        elif size != 19:
            response = {
                'Error': 'Board incomplete',
                'Hexes': serializer.data
            }
            return Response(
                response,
                status=status.HTTP_406_NOT_FOUND
            )
        return Response({'hexes': serializer.data})


class GameViewSets(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GameSerializer
    queryset = Game.objects.all()

    def list_cards_and_resources(self, request, game):
        game = get_object_or_404(Game, pk=game)
        player = get_object_or_404(Player, user=request.user, game=game)
        cards = Card.objects.filter(player=player)
        resources = Resource.objects.filter(player=player)
        data = {'cards': cards, 'resources': resources}
        serializer = self.serializer_class(data)

        return Response(serializer.data)

    def action(self, request, game):
        try:

            player = Player.objects.get(game=game, user=request.user)
            data = request.data['payload']
            action = request.data['type']
            message = getattr(player, action)(data)
            return Response(message,
                            status=status.HTTP_201_CREATED)
        except AttributeError:
            return Response("Bad Request",
                            status=status.HTTP_400_BAD_REQUEST)
        except Game.DoesNotExist:
            return Response(
                "Game does not exist",
                status=status.HTTP_404_NOT_FOUND
            )
        except Vertex.DoesNotExist:
            return Response(
                "Vertex does not exist",
                status=status.HTTP_404_NOT_FOUND
            )
        except Player.DoesNotExist:
            return Response(
                "Player of authenticated user does not exist",
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as error:
            err = str(error)
            # print(err)
            return Response(
                err,
                status=status.HTTP_404_NOT_FOUND
            )
