from django.shortcuts import render
from rest_framework import generics
from .models import Hex
from .serializers import HexSerializer
# Create your views here.


class HexList(generics.ListCreateAPIView):
    serializer_class = HexSerializer

    def get_queryset(self):
        return Hex.objects.filter(game_id=self.kwargs['pk'])
