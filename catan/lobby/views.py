from .models import Room
from .serializers import RoomSerializer
from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class RoomsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        rooms = Room.objects.all()
        list_rooms = [room.id for room in rooms]
        return Response(list_rooms)

    def put(self, request, id):
        return Response([])
