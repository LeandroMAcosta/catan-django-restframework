from django.db import models

from player.models import Player
from utils.constants import RESOURCES


class Resource(models.Model):
    resource = models.CharField(
        max_length=10,
        choices=RESOURCES,
    )
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.resource
