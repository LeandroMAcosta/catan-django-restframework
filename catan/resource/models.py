from django.db import models

from player.models import Player
from utils.constants import RESOURCES


class Resource(models.Model):
    resource = models.CharField(
        max_length=10,
        choices=RESOURCES,
    )
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
    )

    amount = models.PositiveIntegerField(default=0)

    def add(self, value):
        self.amount = self.amount + value

    def decrement(self, value):
        # print(self.resource, self.amount, value)
        if self.amount < value:
            raise Exception('Not enough resources')
        self.amount = self.amount - value

    def __str__(self):
        return self.resource

    class Meta:
        unique_together = ['resource', 'player']
