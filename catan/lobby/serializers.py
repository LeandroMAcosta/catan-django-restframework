from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    players = serializers.StringRelatedField(many=True)
    owner = serializers.StringRelatedField()

    class Meta:
        model = Room
        fields = (
            'id',
            'name',
            'owner',
            'players',
            'max_players',
            'game_has_started',
            'game_id',
        )
