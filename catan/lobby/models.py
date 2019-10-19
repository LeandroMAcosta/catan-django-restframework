from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    board_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner'
    )
    players = models.ManyToManyField(User)
    max_players = models.IntegerField(default=4)
    game_has_started = models.BooleanField(default=False)

    def __str__(self):
        return self.name
