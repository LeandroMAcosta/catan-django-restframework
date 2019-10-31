from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from utils.constants import RESOURCES
from game.models import Game
import random


class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num = models.IntegerField(default=0)
    colour = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    victory_points = models.PositiveIntegerField(default=0)
    # settlements =
    # cities =
    # roads =
    # development_cards =
    # resources_cards =
    # last_gained =

    def get_game(self):
        return self.game

    def available_actions(self):
        # TODO check
        actions = ['build_settlement', 'upgrade_city', 'build_road',
                   'move_robber', 'buy_card', 'play_knight_card',
                   'play_road_building_card', 'play_monopoly_card',
                   'play_year_of_plenty_card', 'end_turn', 'bank_trade']
        return actions

    def get_resource(self, res):
        resource = self.resource_set.get(resource=res)
        return resource

    @staticmethod
    def create_resources(sender, **kwargs):
        job = kwargs.get('instance')
        if kwargs['created']:
            for r in RESOURCES:
                if r[0] == 'desert':
                    continue
                job.resource_set.create(resource=r[0])

    def increase_resources(self, resources):
        resource_list = []
        for resource in resources:
            r = self.get_resource(resource[0])
            r.add(resource[1])
            resource_list.append(r)
        for resource in resource_list:
            resource.save()

    def decrease_resources(self, resources):
        resource_list = []
        for resource in resources:
            r = self.resource_set.get(resource=resource[0])
            r.decrement(resource[1])
            resource_list.append(r)
        for resource in resource_list:
            resource.save()

    def increase_vp(self, amount):
        self.victory_points = models.F('victory_points') + amount
        self.save()

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

        needed_resources = [('brick', 1), ('lumber', 1),
                            ('grain', 1), ('wool', 1)]
        self.decrease_resources(needed_resources)
        self.settlement_set.create(vertex=vertex)
        vertex.used = True
        vertex.save()
        self.increase_vp(1)
        return "Created settlement.", 201

    def check_valid_road(self, v1, v2):
        game = self.game
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
        for pl in game.player_set.all():
            for road in pl.road_set.all():
                if ((road.v1 == vertex1 and road.v2 == vertex2) or
                        (road.v1 == vertex2 and road.v2 == vertex1)):
                    raise Exception("Edge alredy in use")

    def create_road(self, vertex1, vertex2):
        road = self.road_set.create(v1=vertex1, v2=vertex2)
        road.save()

    def purchase_road(self):
        needed_resources = [('brick', 1), ('lumber', 1)]
        self.decrease_resources(needed_resources)

    def build_road(self, data):
        game = self.game
        if len(data) < 2:
            raise Exception("Insufficient arguments")
        elif len(data) > 2:
            raise Exception("Too many arguments")
        v1 = data[0]
        v2 = data[1]
        self.check_valid_road(v1, v2)
        vertex1 = game.vertex_set.get(**v1)
        vertex2 = game.vertex_set.get(**v2)
        self.purchase_road()
        self.create_road(vertex1, vertex2)
        return "Created road.", 201

    def bank_trade(self, data):
        give = data['give']
        receive = data['receive']
        resources = [res[0] for res in RESOURCES]

        if give == receive:
            raise Exception("Resources must be different.")
        elif give not in resources or receive not in resources:
            raise Exception("Resource not exists.")

        resource = self.resource_set.get(resource=give)

        if resource.amount < 4:
            raise Exception("Insufficient resources.")

        new_resource = self.resource_set.get(resource=receive)
        new_resource.add(1)
        resource.decrement(4)

        resource.save()
        new_resource.save()
        return "Trade done.", 200

    def buy_card(self, data):
        cards_types = ['road_building', 'year_of_plenty',
                       'monopoly', 'victory_point', 'knight']
        needed_resources = [('wool', 1), ('grain', 1),  ('ore', 1)]
        self.decrease_resources(needed_resources)
        card = random.randrange(0, 5)
        self.card_set.create(card_type=cards_types[card])

        return "Card purchased", 201

    def end_turn(self, data):
        self.game.end_turn()
        # print(self.game.get_player_turn(), self.game.get_dices())
        return "turn passed ok", 201

    def play_road_building_card(self, data):
        game = self.game
        cards = self.card_set.filter(card_type='road_building')
        if cards.count() == 0:
            raise Exception("Without card")
        card = cards.first()
        if len(data) < 2:
            raise Exception("Insufficient arguments")
        elif len(data) > 2:
            raise Exception("Too many arguments")
        for road_data in data:
            if len(road_data) < 2:
                raise Exception("Insufficient arguments")
            elif len(road_data) > 2:
                raise Exception("Too many arguments")
        for road_data in data:
            v1 = road_data[0]
            v2 = road_data[1]
            self.check_valid_road(v1, v2)
        for road_data in data:
            v1 = road_data[0]
            v2 = road_data[1]
            vertex1 = game.vertex_set.get(**v1)
            vertex2 = game.vertex_set.get(**v2)
            self.create_road(vertex1, vertex2)
        card.delete()
        return "Created road.", 201

    def __str__(self):
        return str(self.user)


post_save.connect(Player.create_resources, sender=Player)
