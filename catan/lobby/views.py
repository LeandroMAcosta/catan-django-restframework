from .models import Room
from .serializers import RoomSerializer
from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)


class RoomsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        query_set = Room.objects.all()
        rooms_serializer = RoomSerializer(query_set, many=True)
        return Response(rooms_serializer.data)

    def put(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
            user = User.objects.get(id=request.user.id)

            if user in room.players.all():
                return Response('Already in the ROOM',
                                status=status.HTTP_200_OK)
            if(room.players.all().count() >= room.max_players):
                return Response('The ROOM is full',
                                status=status.HTTP_200_OK)
        except:
            return Response('The ROOM does not exist',
                            status=status.HTTP_404_NOT_FOUND)

        room.players.add(user)
        return Response(status=status.HTTP_200_OK)
