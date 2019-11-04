from rest_framework import serializers

from .models import Hexagon


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
