from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response 
from .models import Hex
from .serializers import HexSerializer
# Create your views here.


class HexList(generics.ListCreateAPIView):
    serializer_class = HexSerializer

    def get_queryset(self):
        hex_list = Hex.objects.filter(game_id=self.kwargs['pk'])
        return hex_list