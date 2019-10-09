from django.db import models
from player.models import Player


class Resource(models.Model):
    RESOURCES_CHOICES = [
        ('brick', 'Wool'),
        ('lumber', 'Lumber'),
        ('wool', 'Brick'),
        ('grain', 'Grain'),
        ('ore', 'Ore')
    ]
    resource = models.CharField(
        max_length=10,
        choices=RESOURCES_CHOICES,
    )
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.resource
