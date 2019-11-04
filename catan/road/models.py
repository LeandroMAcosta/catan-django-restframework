from django.db import models
from django.core.exceptions import ValidationError
# from player.models import Player
# from game.models import Vertex


class Road(models.Model):
    owner = models.ForeignKey('player.Player', on_delete=models.CASCADE)
    v1 = models.ForeignKey(
        'game.Vertex', on_delete=models.CASCADE, related_name='road_in')
    v2 = models.ForeignKey(
        'game.Vertex', on_delete=models.CASCADE, related_name='road_out')

    def __str__(self):
        return "Road {0} {1} {2}"
        return "Road " + str(self.v1) + " " + str(self.v2) + " from "
        + str(self.owner)

    def clean(self):
        road_v1_v2 = Road.objects.filter(
            v1=self.v1, v2=self.v2).exclude(id=self.id)
        road_v2_v1 = Road.objects.filter(
            v1=self.v2, v2=self.v1)
        if road_v1_v2.exists() or road_v2_v1.exists():
            raise ValidationError({'Exception': 'Edge already in use'})

    class Meta:
        unique_together = ['owner', 'v1', 'v2']
