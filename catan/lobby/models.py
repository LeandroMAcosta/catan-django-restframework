from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User,
        default="",
        to_field='username',
        on_delete=models.CASCADE
    )
    players = models.ManyToManyField(
        User,
        # Ver que onda esta linea
        related_name='%(class)s_id'
    )
    max_players = models.IntegerField(default=4)
