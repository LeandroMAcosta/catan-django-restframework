from django.db import models
from enum import Enum

RESOURCES = (
    ('WO', 'Wool'),
    ('LU', 'Lumber'),
    ('BR', 'Brick'),
    ('GR', 'Grain'),
    ('OR', 'Ore'),
    ('NO', 'Nothing'),
)


class VertexPosition(models.Model):
    level = models.PositiveIntegerField(default=0)
    index = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['level', 'index']

    def __str__(self):
        return '(' + str(self.level) + ',' + str(self.index) + ')'


class Hex(models.Model):
    # game will be a Foreign key to a board/game/room
    game_id = models.IntegerField(default=0)
    position = models.ForeignKey(VertexPosition, on_delete=models.CASCADE)
    resource = models.CharField(max_length=2, choices=RESOURCES, default='NO')
    token = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['game_id', 'position']

    def __str__(self):
        v = self.position
        return 'Game ' + str(self.game_id) + ' ' + str(v)
# Create your models here.
