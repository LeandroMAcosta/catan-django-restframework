from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    players = serializers.StringRelatedField(many=True)

    class Meta:
        model = Room
        fields = '__all__'
