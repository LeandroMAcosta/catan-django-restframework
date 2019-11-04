from django.db import models

from player.models import Player
from utils.constants import RESOURCES

from .exceptions import NotEnoughResourcesException


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

    def decrement(self, value=1):
        if self.amount < value:
            raise NotEnoughResourcesException('Not enough resources')
        self.amount = self.amount - value

    def set(self, value):
        if value < 0:
            raise Exception("Invalid")
        self.amount = value

    def __str__(self):
        return self.resource

    class Meta:
        unique_together = ['resource', 'player']
