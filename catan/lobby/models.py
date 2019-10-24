from django.db import models
from django.contrib.auth.models import User
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

    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
    )

    def number_of_players(self):
        return self.players.all().count()

    def __str__(self):
        return self.name
