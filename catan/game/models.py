from django.db.models.signals import post_save
from django.db import models
import random

from board.models import Hexagon


class Game(models.Model):
    room = models.OneToOneField(
        "lobby.Room",
        on_delete=models.CASCADE
    )
    dice1 = models.IntegerField(default=random.randint(1, 6))
    dice2 = models.IntegerField(default=random.randint(1, 6))
    thief = models.ForeignKey(
        Hexagon,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if self.thief is None:
            board = self.get_board()
            self.thief = board.get_desert()
        super(Game, self).save(*args, **kwargs)

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

    def __str__(self):
        return str(self.id)


post_save.connect(Game.create_vertex, sender=Game)
