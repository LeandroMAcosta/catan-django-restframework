from rest_framework import serializers

from .models import Player


class PlayerSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()

    class Meta:
        model = Player
        fields = '__all__'
