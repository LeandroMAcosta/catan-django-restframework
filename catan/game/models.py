from django.db import models
# from board.models import Vertex


class Game(models.Model):

    def __str__(self):
        return str(self.id)

    def get_board(self):
        return self.room.board

    # def create(self, validated_data):
    #     game = super(Game, self).create(**validated_data)
    #     vertex_data = {
    #         "game": game,
    #         "index": 0,
    #         "level": 5,
    #     }
    #     Vertex.objects.create(**vertex_data)
    #     return game

    # def create(self, *args, **kwargs):
    #     data = {
    #         "game": self.pk,
    #         "index": 0,
    #         "level": 0,
    #     }
    #     Vertex.objecs.create(**data)
    #     super(Game, self).create(*args, **kwargs)
