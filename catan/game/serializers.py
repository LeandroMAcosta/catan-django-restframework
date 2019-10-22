from rest_framework import serializers

from .models import Game


class GameSerializer(serializers.ModelSerializer):
    resources = serializers.StringRelatedField(many=True)
    cards = serializers.StringRelatedField(many=True)

    class Meta:
        model = Game
        fields = ('cards', 'resources')
