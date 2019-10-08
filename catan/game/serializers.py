from rest_framework import serializers
from game.models import Hex, VertexPosition, Game


class VertexPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = VertexPosition
        fields = ('id', 'level', 'index')


class HexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hex
        fields = ('id', 'game_id', 'position', 'resource', 'token',)


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
