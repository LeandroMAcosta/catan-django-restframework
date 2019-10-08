from rest_framework import serializers
from django.contrib.auth.models import User
from player.models import Player


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()

    class Meta:
        model = Player
        fields = '__all__'
