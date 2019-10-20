from django.db import models


class Game(models.Model):

    def __str__(self):
        return str(self.id)

    def get_board(self):
        return self.room.board
