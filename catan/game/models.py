from django.db.models.signals import post_init
from django.db import models
from board.models import Vertex


class Game(models.Model):

    auxiliar = models.BooleanField(default=False) # testeando signals

    def __str__(self):
        return str(self.id)

    def get_board(self):
        return self.room.board

    @staticmethod
    def create_vertex(sender, **kwargs):
        job = kwargs.get('instance')
        for level in [6, 18, 30]:
            for index in range(level):
                vertex_data = {
                    "game": job,
                    "index": index,
                }
                if level == 6:
                    vertex_data['level'] = 0
                elif level == 18:
                    vertex_data['level'] = 1
                else:
                    vertex_data['level'] = 2
                Vertex.objects.create(**vertex_data)


post_init.connect(Game.create_vertex, sender=Game)
