from django.db import models
from django.contrib.auth.models import User

from game.models import Game
from utils.constants import RESOURCES


class Board(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Vertex(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=0)
    index = models.PositiveIntegerField(default=0)
    used = models.BooleanField(default=False)

    class Meta:
        unique_together = ['game', 'level', 'index']

    def __str__(self):
        return '(' + str(self.level) + ',' + str(self.index) + ')'


class Hexagon(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=0)
    index = models.PositiveIntegerField(default=0)
    token = models.PositiveIntegerField(default=0)

    resource = models.CharField(
        max_length=10,
        choices=RESOURCES,
        default='nothing'
    )

    class Meta:
        unique_together = ['board', 'level', 'index']

    def __str__(self):
        v = '(' + str(self.level) + ',' + str(self.index) + ')'
        return 'Board ' + str(self.board) + ' ' + v
