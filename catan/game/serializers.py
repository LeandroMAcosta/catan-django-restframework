from rest_framework import serializers

from .models import Hex, VertexPosition, Game


class VertexPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = VertexPosition
        fields = ('level', 'index',)


class HexSerializer(serializers.ModelSerializer):

    position = VertexPositionSerializer()

    class Meta:
        model = Hex
        fields = ('position', 'resource', 'token',)


class GameSerializer(serializers.ModelSerializer):
    resources = serializers.StringRelatedField(many=True)
    cards = serializers.StringRelatedField(many=True)

    class Meta:
        model = Game
        fields = ('cards', 'resources')
