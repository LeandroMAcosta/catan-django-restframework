from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Room
from .serializers import RoomSerializer


class RoomAlreadyExist(Exception):
    pass


class NameAlreadyExist(Exception):
    pass


class RoomsView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        try:
            name = request.data["name"]
            board_id = request.data["board_id"]

            if Room.objects.filter(board_id=board_id).exists():
                raise RoomAlreadyExist
            if Room.objects.filter(name=name).exists():
                raise NameAlreadyExist

            Room.objects.create(
                board_id=board_id,
                name=name,
                owner=request.user,
            )
        except RoomAlreadyExist:
            return Response(
                'The room already exists',
                status=status.HTTP_409_CONFLICT
            )
        except NameAlreadyExist:
            return Response(
                'Name already in use',
                status=status.HTTP_409_CONFLICT
            )

        return Response(status=status.HTTP_201_CREATED)

    def list(self, request):
        query_set = Room.objects.all()
        rooms = RoomSerializer(query_set, many=True).data
        return Response(
            rooms,
            status=status.HTTP_200_OK
        )

    def update(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
            user = request.user

            if user in room.players.all():
                return Response(
                    'Already in the ROOM',
                    status=status.HTTP_200_OK
                )
            if room.players.all().count() >= room.max_players:
                return Response(
                    'The ROOM is full',
                    status=status.HTTP_200_OK
                )
        except Exception:
            return Response(
                'The ROOM does not exist',
                status=status.HTTP_404_NOT_FOUND
            )

        room.players.add(user)
        return Response(status=status.HTTP_200_OK)
