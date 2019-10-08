from rest_framework import serializers
from .models import Room
from player.serializers import PlayerSerializer


class RoomSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True)

    class Meta:
        model = Room
        fields = ('id', 'players', 'max_players', 'name', 'owner')
