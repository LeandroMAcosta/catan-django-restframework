from django.db.models.signals import post_save
from django.db import models
from django.db.models import Q
import random

from road.models import Road


class Game(models.Model):
    room = models.OneToOneField(
        "lobby.Room",
        on_delete=models.CASCADE
    )
    player_turn = models.IntegerField(default=0)
    dice1 = models.IntegerField(default=random.randint(1, 6))
    dice2 = models.IntegerField(default=random.randint(1, 6))
    thief = models.ForeignKey(
        'board.Hexagon',
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

    def get_full_dice(self):
        return self.dice1 + self.dice2

    def get_board(self):
        return self.room.board

    def get_hexagon(self, index, level):
        board = self.get_board()
        hexagon = board.hexagon_set.get(index=index, level=level)
        return hexagon

    def get_vertex(self, index, level):
        return self.vertex_set.get(index=index, level=level)

    def get_dices(self):
        return self.dice1, self.dice2

    def get_player_turn(self):
        return self.player_turn

    def get_player_from_username(self, username):
        return self.player_set.get(user__username=username)

    def throw_dice(self):
        self.dice1 = random.randint(1, 6)
        self.dice2 = random.randint(1, 6)
        self.save()

    def end_turn(self):
        self.throw_dice()
        turn = self.player_turn
        number_of_players = self.room.number_of_players()
        self.player_turn = (turn + 1) % number_of_players
        self.save()
        self.distribute_resources()

    def distribute_resources(self):
        dice = self.dice1 + self.dice2
        h = self.room.board.hexagon_set.filter(token=dice)
        for hexag in h:
            ver = hexag.get_neighboring_vertices()
            for v in ver:
                level = v['level']
                index = v['index']
                vertex = self.vertex_set.get(level=level, index=index)
                settl = None
                try:
                    settl = vertex.settlement
                except Exception:
                    continue
                if settl is not None:
                    player = settl.owner
                    r = hexag.resource
                    player.increase_resources([(r, 1)])

    def get_vertex_from_hexagon(self, index, level):
        hexagon = self.get_hexagon(index, level)
        hexagon_vertex = hexagon.get_neighboring_vertices()
        ret = list(map(
                lambda vertex: self.get_vertex(
                    index=vertex['index'],
                    level=vertex['level']
                ),
                hexagon_vertex
            )
        )
        return ret

    def __str__(self):
        return str(self.id)


post_save.connect(Game.create_vertex, sender=Game)


class Vertex(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=0)
    index = models.PositiveIntegerField(default=0)
    # TODO delete this field
    used = models.BooleanField(default=False)

    def get_settlement(self):
        try:
            return self.settlement
        except Exception:
            return None

    def is_used(self):
        return self.get_settlement() is not None

    class Meta:
        unique_together = ['game', 'level', 'index']

    def get_roads(self, vertex=None):
        if vertex is None:
            return Road.objects.filter(Q(v1=self) or Q(v2=self))
        try:
            return Road.objects.get(
                (Q(v1=self) and Q(v2=vertex)) or (Q(v1=vertex) and Q(v2=self))
            )
        except Exception:
            return None

    def can_build_road_of_player(self, player):
        roads = self.get_roads()
        for road in roads:
            if road.owner == player:
                return True
        settlement = self.get_settlement()
        return settlement and settlement.owner == player

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
            vertex = vertex_game.get(level=1, index=index*3)
            neighbors.append(vertex)
        elif level == 1:
            new_level = index % 3
            k = new_level == 2
            vertex = vertex_game.get(
                level=new_level,
                index=k*index + (k+1)*(index+k)//3
            )
            neighbors.append(vertex)
        elif (index - 1) % 5 == 0 or (index + 1) % 5 == 0:
            vertex = vertex_game.get(
                level=1,
                index=index - 2*((1+index)//5)
            )
            neighbors.append(vertex)
        return neighbors

    def __str__(self):
        return "({0}, {1})".format(self.level, self.index)
