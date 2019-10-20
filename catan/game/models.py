from django.db import models

from utils.constants import RESOURCES


class Game(models.Model):

    def __str__(self):
        return str(self.id)


class VertexPosition(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=0)
    index = models.PositiveIntegerField(default=0)
    used = models.BooleanField(default=False)

    class Meta:
        unique_together = ['game_id', 'level', 'index']

    def __str__(self):
        return '(' + str(self.level) + ',' + str(self.index) + ')'


class Hex(models.Model):
    # game_id will be a Foreign key to a board/game/room
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=0)
    index = models.PositiveIntegerField(default=0)

    resource = models.CharField(
        max_length=10,
        choices=RESOURCES,
        default='nothing'
    )
    token = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['game_id', 'level', 'index']

    def __str__(self):
        v = self.position
        return 'Game ' + str(self.game_id) + ' ' + str(v)
