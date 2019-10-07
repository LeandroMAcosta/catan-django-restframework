from django.db import models


# Create your models here.
class Resources(models.Model):
    WOOL = 'WO'
    LUMBER = 'LU'
    BRICK = 'BR'
    GRAIN = 'GR'
    ORE = 'OR'
    NOTHING = 'NO'
    RESOURCES_CHOICES = [
        (WOOL='Wool'),
        (LUMBER='Lumber'),
        (BRICK='Brick'),
        (GRAIN='Grain'),
        (ORE='Ore'),
        (NOTHING='Nothing'),
    ]
    resource = models.CharField(
        choices=RESOURCES_CHOICES,
        default=NOTHING,
        )
    count_resource = models.IntegerField(default=0)
    owner_player = models.ForeignKey(
        player.Player,
        on_delete=models.CASCADE,
        )
