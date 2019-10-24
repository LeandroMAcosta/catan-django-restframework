from django.db import models
from django.core.exceptions import ValidationError
from player.models import Player
from board.models import Vertex


class Road(models.Model):
    owner = models.ForeignKey(Player, on_delete=models.CASCADE)
    v1 = models.ForeignKey(
        Vertex, on_delete=models.CASCADE, related_name='road_in')
    v2 = models.ForeignKey(
        Vertex, on_delete=models.CASCADE, related_name='road_out')

    def __str__(self):
        return "Road " + str(self.v1) + " " + str(self.v2) + " from "
        + str(self.owner)

    def Meta(self):
        unique_together = ['owner', 'v1', 'v2']  # noqa: F841

    def clean(self):
        road_v1_v2 = Road.objects.filter(
            v1=self.v1, v2=self.v2).exclude(id=self.id)
        road_v2_v1 = Road.objects.filter(
            v1=self.v2, v2=self.v1)
        if road_v1_v2.exists() or road_v2_v1.exists():
            raise ValidationError({'Exception': 'Edge already in use'})
