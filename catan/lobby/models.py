from django.db import models

class Room(models.Model):
    #id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100) #Change to USERNAME
    #needs to be a relation between tables 
    #players = [] #Arrays of USERNAMEs
    max_players = models.IntegerField(default=4)


