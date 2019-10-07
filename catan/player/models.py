from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    colour = models.CharField(max_length=100)
    # settlements =
    # cities =
    # roads =
    # development_cards =
    # resources_cards =
    # last_gained =
