from django.db import models
from django.contrib.auth.models import User

from utils.constants import RESOURCES


class Board(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Vertex(models.Model):
    game = models.ForeignKey("game.Game", on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=0)
    index = models.PositiveIntegerField(default=0)
    used = models.BooleanField(default=False)

    class Meta:
        pass
        # unique_together = ['game', 'level', 'index']

    def get_neighbors(self):
        vertex_game = Vertex.objects.filter(game=self.game)
        level = self.level
        index = self.index
        limit = [6, 18, 30]
        neighbors = []

        # Neighbors of the same level
        neighbors.append(
            vertex_game.get(level=level, index=(index-1) % limit[level])
        )
        neighbors.append(
            vertex_game.get(level=level, index=(index+1) % limit[level])
        )

        # Neighbors of other level
        if level == 0:
            neighbors.append(vertex_game.get(level=1, index=index*3))
        elif level == 1:
            if index % 3 == 0:
                neighbors.append(
                    vertex_game.get(level=0, index=index//3)
                )
            else:
                neighbors.append(
                    vertex_game.get(level=1, index=index + 2*((index+1)//3))
                )
        else:
            if (index - 1) % 5 == 0 or (index + 1) % 5 == 0:
                neighbors.append(
                    vertex_game.get(level=1, index=index - 2*((1+index)//5))
                )
        return neighbors

    def __str__(self):
        return '(' + str(self.level) + ',' + str(self.index) + ')'


class Hexagon(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=0)
    index = models.PositiveIntegerField(default=0)
    token = models.PositiveIntegerField(default=0)

    resource = models.CharField(
        max_length=10,
        choices=RESOURCES,
        default='nothing'
    )

    class Meta:
        unique_together = ['board', 'level', 'index']

    def __str__(self):
        v = '(' + str(self.level) + ',' + str(self.index) + ')'
        return 'Board ' + str(self.board) + ' ' + v
