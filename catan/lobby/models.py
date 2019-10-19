from django.db import models
from django.contrib.auth.models import User
from game.models import Game
from board.models import Board


class Room(models.Model):
    name = models.CharField(max_length=100)
    players = models.ManyToManyField(User)
    max_players = models.IntegerField(default=4)
    game_has_started = models.BooleanField(default=False)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner'
    )
    game_id = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
