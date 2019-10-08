from django.shortcuts import render
from rest_framework.response import Response
from .models import Hex
from .serializers import HexSerializer
from rest_framework import permissions, viewsets, status
from game.serializers import GameSerializer
from card.serializers import CardSerializer
from card.models import Card
# from resource.models import Resource


class HexListViewSets(viewsets.ViewSet):

    def list(self, request, game_id=None):
        queryset = Hex.objects.filter(game_id=game_id)
        serializer = HexSerializer(queryset, many=True)
        return Response({'hexes': serializer.data})


class GameViewSets(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GameSerializer
    queryset = Card.objects.all()

    def resources(self, request, pk=None):
        try:
            cards = Card.objects.filter(player__user=request.user)
            card_serializer = CardSerializer(cards, many=True)

            # resources = Resource.objects.filter(player__user=request.user)
            # resource_serializer = ResourceSerializer(cards, many=True)

            return Response({
                'cards': serializer.data,
                'resources': [],
            })
        except Exception as e:
            return Response(status=status.django)
