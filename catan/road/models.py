from django.db import models
from player.models import Player
from board.models import Vertex


class Road(models.Model):
    owner = models.ForeignKey(Player, on_delete=models.CASCADE)
    vertexes = models.ManyToManyField(Vertex)

    def __str__(self):
        s = set()
        vert = self.vertexes.all()
        for v in vert:
            s.add(str(v))
        return "Road " + str(s) + " from " + str(self.owner)
