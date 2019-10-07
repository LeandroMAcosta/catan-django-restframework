from django.shortcuts import render
from rest_framework import permissions, viewsets
from game.serializers import GameSerializer


class GameViewSets(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GameSerializer
