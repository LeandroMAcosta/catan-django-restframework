from django.db import models
from player.models import Player


class Card(models.Model):
    CARD_TYPE = [
        ('road_building', 'Road building'),
        ('year_of_plenty', 'Year of plenty'),
        ('monopoly', 'Monopoly'),
        ('victory_point', 'Victory point'),
        ('knight', 'Knight')
    ]
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    card_type = models.CharField(max_length=30, choices=CARD_TYPE)

    def __str__(self):
        return self.card_type
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import permissions, viewsets, status
from game.serializers import GameSerializer
from card.serializers import CardSerializer
from card.models import Card
# from resource.models import Resource