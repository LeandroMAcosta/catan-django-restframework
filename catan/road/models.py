from django.db import models
from player.models import Player
from board.models import Vertex


class Road(models.Model):
    owner = models.ForeignKey(Player, on_delete=models.CASCADE)
    v1 = models.ForeignKey(
        Vertex, on_delete=models.CASCADE, related_name='road_in')
    v2 = models.ForeignKey(
        Vertex, on_delete=models.CASCADE, related_name='road_out')

    def get_owner(self):
        return self.owner

    def get_game(self):
        return self.owner.get_game()

    def __str__(self):
        return "Road {0} {1} {2}"
        return "Road " + str(self.v1) + " " + str(self.v2) + " from "
        + str(self.owner)

    class Meta:
        unique_together = ['owner', 'v1', 'v2']
