from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    players = serializers.StringRelatedField()

    class Meta:
        model = Room
        fields = ('id', 'players', 'max_players', 'name', 'owner')
