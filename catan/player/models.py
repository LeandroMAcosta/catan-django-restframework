from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from utils.constants import RESOURCES
from game.models import Game
import random

from game.exceptions import ActionExceptionError


class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num = models.IntegerField(default=0)
    colour = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    victory_points = models.PositiveIntegerField(default=0)

    def get_game(self):
        return self.game

    def available_actions(self):
        """
        This method verifies all possible actions that the player can do
        :returns:
            - available_actions - list of json with available actions from
                player, for the endpoint GET game/:pk/player/actions
            - actions - list of string with available actions from player,
                to check that the action sent by post is available
        """
        available_actions = []
        current_turn = self.game.get_player_turn()
        my_turn = self.num

        if current_turn == my_turn:
            # buil_settlement
            # TODO It can only be when there are roads
            payload = []

            vertices = self.game.vertex_set.all()
            for vertex in vertices:
                if not vertex.is_used():
                    payload.append({
                        "index": vertex.index,
                        "level": vertex.level
                    })

            available_actions.append({
                "type": "build_settlement",
                "payload": payload
            })

            # upgrade_city
            payload = []
            for vertex in vertices:
                if vertex.used and not vertex.settlement.upgrade:
                    payload.append(vertex)

            if payload:
                available_actions.append({
                    "type": "upgrade_city",
                    "payload": payload
                })

            # move_robber and play_knight_card

            if self.game.get_full_dice() == 7 or \
               self.card_set.filter(card_type="knight").exists():

                payload = []
                game = self.game
                board = game.get_board()
                hexagons = board.hexagon_set.all()
                for hexagon in hexagons:
                    index = hexagon.index
                    level = hexagon.level
                    vertices = game.get_vertex_from_hexagon(index, level)
                    data = {
                        "position": {
                            "index": index,
                            "level": level
                        },
                        "players": []
                    }
                    for vertex in vertices:
                        is_used = vertex.is_used()
                        if is_used and vertex.settlement.owner != self:
                            player = vertex.settlement.owner.user.username
                            data["players"].append(player)
                    payload.append(data)

                if self.game.get_full_dice() == 7:
                    available_actions.append({
                        "type": "move_robber",
                        "payload": payload
                    })

                if self.card_set.filter(card_type="knight").exists():
                    available_actions.append({
                        "type": "play_knight_card",
                        "payload": payload
                    })

            # buy_card
            wool = self.get_resource('wool').amount
            grain = self.get_resource('grain').amount
            ore = self.get_resource('ore').amount

            if wool > 0 and grain > 0 and ore > 0:
                available_actions.append({
                    "type": "buy_card",
                    "payload": None
                })

            # end_turn
            available_actions.append({
                "type": "end_turn",
                "payload": None
            })

            # bank_trade
            resource = self.resource_set.filter(amount__gte=4)

            if resource.exists():
                available_actions.append({
                    "type": "bank_trade",
                    "payload": None
                })

            # TODO play_road_building_card 6
            # TODO play_monopoly_card 7
            # TODO play_year_of_plenty_card 8
            # TODO build_road 2 (importante para los test @mateo)

        actions = set([action["type"] for action in available_actions])
        return available_actions, actions

    def get_cities(self):
        return self.settlement_set.all()

    def get_roads(self):
        return self.road_set.all()

    def get_total_resources(self):
        resources = self.resource_set.all()
        return sum(map(lambda resource: resource.amount, resources))

    def get_resource(self, res):
        return self.resource_set.get(resource=res)

    def get_resource_amount(self, res):
        resource = self.resource_set.get(resource=res)
        return resource.amount

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

    def decrement_random_resource(self):
        total_resources = self.get_total_resources()
        if total_resources <= 0:
            raise ActionExceptionError("Not enough resources.")
        resources = self.resource_set.filter(amount__gt=0)
        resource = random.choice(resources)
        resource.decrement()
        resource.save()
        return resource

    def remove_random_resources(self, amount):
        while amount > 0:
            self.decrement_random_resource()
            amount -= 1

    # Actions methods
    def move_robber(self, data, knight_card=False):

        game = self.game
        player_to_steal = data.get('player', None)
        position = data.get('position', None)
        index = position['index']
        level = position['level']
        hexagon = game.get_hexagon(index, level)
        game.thief = hexagon

        # Only for move robber
        if not knight_card:
            if game.get_full_dice() != 7:
                raise ActionExceptionError("Sum of dices must be equal to 7.")

            players = game.player_set.all()
            for p in players:
                total = p.get_total_resources()
                if total > 7:
                    p.remove_random_resources(total//2)

        # Steal player
        if player_to_steal is not None:
            stolen_player = game.get_player_from_username(player_to_steal)
            hexagon = game.get_hexagon(index, level)
            vertices = game.get_vertex_from_hexagon(index, level)

            for vertex in vertices:
                settlement = vertex.get_settlement()
                if settlement and settlement.owner == stolen_player:
                    stolen_resource = stolen_player.decrement_random_resource()
                    stolen_resource.save()
                    resource = self.get_resource(stolen_resource.resource)
                    resource.add(1)
                    resource.save()
                    game.save()
                    return "Thief positioned and Player stolen.", 200
            raise ActionExceptionError("Player not in hexagon.")

        game.save()
        return "Thief positioned.", 200

    def play_knight_card(self, data):
        return self.move_robber(data, knight_card=True)

    def increase_vp(self, amount):
        self.victory_points = models.F('victory_points') + amount
        self.save()

    def build_settlement(self, data):
        # TODO check neighbours
        game = self.game
        limit = [6, 18, 30]
        level = data['level']
        index = data['index']
        if not (0 <= level < 3 and 0 <= index < limit[level]):
            raise ActionExceptionError("Index or level out of bounds.")

        vertex = game.vertex_set.get(**data)
        if vertex.used:
            raise ActionExceptionError("Vertex alredy in use.")

        needed_resources = [('brick', 1), ('lumber', 1),
                            ('grain', 1), ('wool', 1)]
        self.decrease_resources(needed_resources)
        self.settlement_set.create(vertex=vertex)
        vertex.used = True
        vertex.save()
        self.increase_vp(1)
        return "Created settlement.", 201

    def build_road(self, data):
        game = self.game
        if len(data) < 2:
            raise ActionExceptionError("Insufficient arguments")
        elif len(data) > 2:
            raise ActionExceptionError("Too many arguments")
        v1 = data[0]
        v2 = data[1]
        limit = [6, 18, 30]
        if not (0 <= v1['level'] < 3 and 0 <= v2['level'] < 3):
            raise ActionExceptionError("Level out of bounds")
        if not (0 <= v1['index'] < limit[v1['level']]
                and 0 <= v2['index'] < limit[v2['level']]):
            raise ActionExceptionError("Index out of bounds.")
        vertex1 = game.vertex_set.get(**v1)
        vertex2 = game.vertex_set.get(**v2)
        if not (vertex2 in vertex1.get_neighbors()):
            raise ActionExceptionError("Non adjacent or repeated vertexes.")
        needed_resources = [('brick', 1), ('lumber', 1)]
        self.decrease_resources(needed_resources)
        resource = self.road_set.create(v1=vertex1, v2=vertex2)
        resource.clean()
        resource.save()
        return "Created road.", 201

    def bank_trade(self, data):
        give = data['give']
        receive = data['receive']
        resources = [res[0] for res in RESOURCES]

        if give == receive:
            raise ActionExceptionError("Resources must be different.")
        elif give not in resources or receive not in resources:
            raise ActionExceptionError("Resource not exists.")

        resource = self.resource_set.get(resource=give)

        if resource.amount < 4:
            raise ActionExceptionError("Insufficient resources.")

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
        # print("player turn: ", self.game.get_player_turn())
        # print("dices: ", self.game.get_dices())
        return "turn passed ok", 201

    def __str__(self):
        return str(self.user)


post_save.connect(Player.create_resources, sender=Player)
