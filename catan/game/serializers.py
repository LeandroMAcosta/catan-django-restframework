from rest_framework import serializers

from .models import Game, Vertex


class GameSerializer(serializers.ModelSerializer):
    resources = serializers.StringRelatedField(many=True)
    cards = serializers.StringRelatedField(many=True)

    class Meta:
        model = Game
        fields = ('cards', 'resources', 'player_turn', 'dice1', 'dice2')


class VertexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vertex
        fields = ('level', 'index',)
