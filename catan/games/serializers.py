from rest_framework import serializers
from .models import Hex, VertexPosition


class VertexPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = VertexPosition
        fields = ('id', 'level', 'index')


class HexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hex
        fields = ('id', 'game_id', 'position', 'resource', 'token',)
