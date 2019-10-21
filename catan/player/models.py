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
        vertex = game.vertex_set.get(**data)

        if vertex.used:
            raise Exception("Vertex alredy in use.")

        self.settlement_set.create(
            vertex=vertex
        )
        vertex.used = True
        vertex.save()

    def __str__(self):
        return str(self.user)
