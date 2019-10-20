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

    def create(self, request):
        try:
            name = request.data["name"]
            board_id = request.data["board_id"]

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
                status=status.HTTP_409_CONFLICT
            )
        except NameAlreadyExist:
            return Response(
                'Name already in use',
                status=status.HTTP_409_CONFLICT
            )
        except BoardNotExist:
            return Response(
                'The Board not exist',
                status=status.HTTP_409_CONFLICT
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

    def join(self, request, room_id):
        try:
            if not Room.objects.filter(id=room_id).exists():
                raise RoomNotExist

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
        except RoomNotExist:
            return Response(
                'The ROOM does not exist',
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            return Response(
                'BADREQUEST',
                status=status.HTTP_400_BAD_REQUEST
            )

        room.players.add(user)
        return Response(status=status.HTTP_200_OK)

    def start_game(self, request, room_id):
        try:
            query_set = Room.objects.get(id=room_id)
        except Exception:
            return Response(
                'The ROOM does not exist',
                status=status.HTTP_404_NOT_FOUND
            )

        if query_set.game_has_started:
            return Response(
                "The game has started",
                status=status.HTTP_200_OK
            )
        room = RoomSerializer(query_set).data
        if len(room['players']) < 3 or len(room['players']) > 4:
            return Response(
                "3 or 4 players are required",
                status=status.HTTP_200_OK
            )
        colours = ['red', 'green', 'blue', 'yellow']
        # Cuando hagamos Game hacemos esta parte
        game = Game.objects.get_or_create()

        for colour, user in enumerate(room['players']):
            Player.objects.create(
                user=User.objects.get(username=user),
                colour=colours[colour],
                game=game
            )
        query_set.game_has_started = True
        query_set.save()

        return Response(status=status.HTTP_200_OK)

    def cancel_lobby(self, request, room_id):
        try:
            query_set = Room.objects.get(id=room_id)
            query_set.delete()
        except Exception:
            return Response(
                'The ROOM does not exist',
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(status=status.HTTP_200_OK)
