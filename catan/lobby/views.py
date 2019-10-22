from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from .models import Room
from board.models import Board
from player.models import Player
from game.models import Game
from .serializers import RoomSerializer

from .exeptions import (
    RoomAlreadyExist,
    RoomNotExist,
    NameAlreadyExist,
    BoardNotExist,
)


class RoomsView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Room.objects.all()

    def create(self, request, name, board_id):
        try:
            if Room.objects.filter(board_id=board_id).exists():
                raise RoomAlreadyExist
            if Room.objects.filter(name=name).exists():
                raise NameAlreadyExist
            if not Board.objects.filter(id=board_id).exists():
                raise BoardNotExist

            board = Board.objects.get(id=board_id)
            Room.objects.create(
                board=board,
                name=name,
                owner=request.user,
            )
        except RoomAlreadyExist:
            return Response(
                'The room already exists',
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        except NameAlreadyExist:
            return Response(
                'Name already in use',
                status=status.HTTP_409_CONFLICT
            )
        except BoardNotExist:
            return Response(
                'The Board not exist',
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        except Exception:
            return Response(
                'BADREQUEST',
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(status=status.HTTP_201_CREATED)

    def list(self, request):
        query_set = Room.objects.all()
        rooms = RoomSerializer(query_set, many=True).data
        return Response(
            rooms,
            status=status.HTTP_200_OK
        )

    def join(self, request, pk):
        try:
            if not Room.objects.filter(id=pk).exists():
                raise RoomNotExist

            room = Room.objects.get(id=pk)
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
        except RoomNotExist:
            return Response(
                'The ROOM does not exist',
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        except Exception:
            return Response(
                'BADREQUEST',
                status=status.HTTP_400_BAD_REQUEST
            )

        room.players.add(user)
        return Response(status=status.HTTP_200_OK)

    def start_game(self, request, pk=None):

        room = self.get_object()

        if room.game_has_started:
            return Response(
                "The game has started",
                status=status.HTTP_200_OK
            )

        if not (3 < room.number_of_players() < 4):
            return Response(
                "3 or 4 players are required",
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

        room.start_game()

        return Response(status=status.HTTP_200_OK)

    def cancel_lobby(self, request, pk):
        try:
            query_set = Room.objects.get(id=pk)
            query_set.delete()
        except Exception:
            return Response(
                'The ROOM does not exist',
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        return Response(status=status.HTTP_200_OK)
