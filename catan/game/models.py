from django.db.models.signals import post_init
from django.db import models


class Game(models.Model):

    def __str__(self):
        return str(self.id)

    def get_board(self):
        return self.room.board

    @staticmethod
    def create_vertex(sender, **kwargs):
        job = kwargs.get('instance')
        job.save()
        if job:
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
                    job.vertex_set.create(**vertex_data)


post_init.connect(Game.create_vertex, sender=Game)
