from rest_framework import serializers
from .models import Room
from player.serializers import UsernameSerializer


class RoomSerializer(serializers.ModelSerializer):
    players = serializers.StringRelatedField(many=True)

    class Meta:
        model = Room
        fields = '__all__'
