from django.db import models


class Game(models.Model):

    def __str__(self):
        return self.id
