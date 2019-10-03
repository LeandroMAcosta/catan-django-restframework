from django.db import models

class ROOM(models.Model):
    #id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100) #Change to USERNAME
    players = [] #Arrays of USERNAMEs
    max_players = models.IntegerField(default=4)

    def join_room(p):
        if(len(this.players) < this.max_players):
            this.players.append(p)

