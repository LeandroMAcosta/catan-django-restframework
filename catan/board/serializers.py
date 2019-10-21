from rest_framework import serializers

from .models import Hexagon, Vertex


class VertexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vertex
        fields = ('level', 'index',)


class HexagonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hexagon
        fields = ('level', 'index', 'resource', 'token',)
