from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Hex
from .serializers import HexSerializer
# Create your views here.


class HexList(viewsets.ViewSet):

    def list(self, request, game_id=None):
        queryset = Hex.objects.filter(game_id=game_id)
        serializer = HexSerializer(queryset, many=True)
        return Response({'hexes': serializer.data})
