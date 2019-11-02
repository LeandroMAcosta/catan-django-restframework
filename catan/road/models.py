from django.db import models
from django.core.exceptions import ValidationError
from player.models import Player


class Road(models.Model):
    owner = models.ForeignKey(Player, on_delete=models.CASCADE)
    v1 = models.ForeignKey(
        'board.Vertex', on_delete=models.CASCADE, related_name='road_1')
    v2 = models.ForeignKey(
        'board.Vertex', on_delete=models.CASCADE, related_name='road_2')

    def get_owner(self):
        return self.owner

    def get_game(self):
        return self.owner.get_game()

    def __str__(self):
        return "Road {0} {1} {2}"
        return "Road " + str(self.v1) + " " + str(self.v2) + " from "
        + str(self.owner)

    def clean(self):
        road_v1_v2 = Road.objects.filter(
            v1=self.v1, v2=self.v2,
            owner__game=self.get_game()).exclude(id=self.id)
        road_v2_v1 = Road.objects.filter(
            v1=self.v2, v2=self.v1, owner__game=self.get_game())
        if road_v1_v2.exists() or road_v2_v1.exists():
            raise ValidationError({'Exception': 'Edge already in use'})

    class Meta:
        unique_together = ['owner', 'v1', 'v2']
