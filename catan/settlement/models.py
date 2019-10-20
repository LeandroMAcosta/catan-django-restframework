from django.db import models
from player.models import Player
from board.models import Vertex


class Settlement(models.Model):
    owner = models.ForeignKey(Player, on_delete=models.CASCADE)
    upgrade = models.BooleanField(default=False)
    vertex = models.OneToOneField(
        Vertex,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(str(self.vertex) + " from " + str(self.owner))
