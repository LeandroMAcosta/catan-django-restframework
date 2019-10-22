import random

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
        return "Created settlement."

    def build_road(self, data):
        game = self.game
        if len(data) < 2:
            raise Exception("Insufficient arguments")
        elif len(data) > 2:
            raise Exception("Too many arguments")
        v1 = data[0]
        v2 = data[1]
        limit = [6, 18, 30]
        if not (0 <= v1['level'] < 3 and 0 <= v2['level'] < 3):
            raise Exception("Level out of bounds")
        if not (0 <= v1['index'] < limit[v1['level']]
                and 0 <= v2['index'] < limit[v2['level']]):
            raise Exception("Index out of bounds.")
        vertex1 = game.vertex_set.get(**v1)
        vertex2 = game.vertex_set.get(**v2)
        if not (vertex2 in vertex1.get_neighbors()):
            raise Exception("Non adjacent or repeated vertexes.")
        r = self.road_set.create(v1=vertex1, v2=vertex2)
        r.clean()
        r.save()
        return "Created road."

    def buy_card(self, data):
        cards_types = ['road_building', 'year_of_plenty',
                       'monopoly', 'victory_point', 'knight']
        cnumber = random.randrange(0, 5)
        self.card_set.create(card_type=cards_types[cnumber])
        # for c in self.card_set.all():
        #     print(str(c))
        return "Card purchased"

    def __str__(self):
        return str(self.user)
