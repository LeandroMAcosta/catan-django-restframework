from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Card(models.Model):
    CARD_TYPE = [
        ('rb', 'Road building'),
        ('yp', 'Year of plenty'),
        ('m', 'Monopoly'),
        ('vp', 'Victory point'),
        ('k', 'Knight')
    ]
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    card_type = models.CharField(max_length=2, choices=CARD_TYPE)
