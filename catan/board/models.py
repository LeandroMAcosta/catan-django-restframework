from django.contrib.auth.models import User
from django.db import models

from utils.constants import RESOURCES


class Board(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def get_desert(self):
        return self.hexagon_set.get(resource='desert') or None

    def __str__(self):
        return self.name


class Hexagon(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=0)
    index = models.PositiveIntegerField(default=0)
    token = models.PositiveIntegerField(default=0)

    resource = models.CharField(
        max_length=10,
        choices=RESOURCES,
        default='desert'
    )

    class Meta:
        unique_together = ['board', 'level', 'index']

    def __str__(self):
        v = "({0} {1})".format(self.level, self.index)
        return "Board {0} {1}".format(self.board, v)

    def get_neighboring_vertices(self):
        level = self.level
        index = self.index
        neighbours = []
        if level == 0:
            for i in range(0, 6):
                neighbours.append((0, i))
        elif level == 1:
            for i in range(0, 2):
                neighbours.append((0, (index + i) % 6))
            for i in range(0, 4):
                neighbours.append((1, (3*index + i) % 18))
        else:
            if index % 2 == 0:
                for i in range(-1, 2):
                    neighbours.append((1, (index + index//2 + i) % 18))
                for i in range(-1, 2):
                    neighbours.append((2, (2*index + index//2 + i) % 30))
            else:
                for i in range(0, 2):
                    neighbours.append((1, (index + index//2 + i) % 18))
                for i in range(-1, 3):
                    neighbours.append((2, (2*index + index//2 + i) % 30))

        def pack_to_dict(vertex):
            return({'level': vertex[0],
                    'index': vertex[1]
                    })
        return map(pack_to_dict, neighbours)
