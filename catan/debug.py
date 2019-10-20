from django.contrib.auth import authenticate

from lobby.models import Room
from game.models import Game
from board.models import Board

user = authenticate(username='admin', password='admin123')
board = Board(name='boardsito', owner=user)
board.save()
room = Room(name="nombresito", owner=user, board=board)
room.save()
game = Game(room=room)
game.save()
