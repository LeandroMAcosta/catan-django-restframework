from django.db.models.signals import post_save
from django.db import models
import random


class Game(models.Model):
    room = models.OneToOneField(
        "lobby.Room",
        on_delete=models.CASCADE
    )
    dice1 = models.IntegerField(default=random.randint(1, 6))
    dice2 = models.IntegerField(default=random.randint(1, 6))

    @staticmethod
    def create_vertex(sender, **kwargs):
        job = kwargs.get('instance')
        if kwargs['created']:
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

    def get_board(self):
        return self.room.board

    def throw_dice(self):
        self.dice1 = random.randint(1, 6)
        self.dice2 = random.randint(1, 6)
        self.save()
        return (self.dice1, self.dice2)

    def distribute_resources(self):
        dice = self.dice1 + self.dice2
        h = self.room.board.hexagon_set.filter(token=dice)
        for hexag in h:
            ver = hexag.get_neighboring_vertexes()
            for v in ver:
                level = v[0]
                index = v[1]
                vertex = self.vertex_set.get(level=level, index=index)
                settl = vertex.settlement
                if settl is not None:
                    player = settl.owner
                    r = hexag.resources
                    player.increase_resources([(r, 1)])

    def __str__(self):
        return str(self.id)


post_save.connect(Game.create_vertex, sender=Game)
