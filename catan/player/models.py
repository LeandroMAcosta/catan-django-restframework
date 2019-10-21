from django.db import models
from django.contrib.auth.models import User

from game.models import Game
# from settlement.models import Settlement


class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    colour = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    # settlements =
    # cities =
    # roads =
    # development_cards =
    # resources_cards =
    # last_gained =

    def build_settlement(self, data):
        game = self.game
        limit = [6, 18, 30]
        level = data['level']
        index = data['index']
        if not (0 <= level < 3 and 0 <= index < limit[level]):
            raise Exception("Index or level out of bounds.")

        vertex = game.vertex_set.get(**data)
        if vertex.used:
            raise Exception("Vertex alredy in use.")

        self.settlement_set.create(
            vertex=vertex
        )
        vertex.used = True
        vertex.save()

    # def build_road(self, data):
    #     game = self.game
    #     v1 = data.first
    #     v2 = data.second
    #     limit = [6, 18, 30]
    #     if not (0 <= v1['level'] < 3 and 0 <= v2['level'] < 3):
    #         raise Exception("Level out of bounds")
    #     if not (0 <= v1['index'] < limit[v1['level']]
    #             and 0 <= v2['index'] < limit[v2['level']]):
    #         raise Exception("Index out of bounds")
    #     vertex1 = game.vertex_set.get(**data.first)
    #     vertex2 = game.vertex_set.get(**data.second)
    #     if not (vertex2 in vertex1.get_neighbors())
    #     r = self.road_set.create()
    #     r.vertexes.add(vertex1, vertex2)
    #     r.save()

    def __str__(self):
        return str(self.user)
