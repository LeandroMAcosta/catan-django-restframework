from django.db import models


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
