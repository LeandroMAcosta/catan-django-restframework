from rest_framework import serializers

from .models import Hexagon, Vertex


class VertexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vertex
        fields = ('level', 'index',)


class HexagonSerializer(serializers.ModelSerializer):
    position = serializers.SerializerMethodField()

    def get_position(self, instance):
        return {
            'index': instance.index,
            'level': instance.level
        }

    class Meta:
        model = Hexagon
        fields = ('resource', 'token', 'position')
