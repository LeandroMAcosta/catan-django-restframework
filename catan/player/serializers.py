from rest_framework import serializers
from django.contrib.auth.models import User
from player.models import Player


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email')


class PlayerSerializer(serializers.ModelSerializer):
    # user = UserSerializer()

    class Meta:
        model = Player
        fields = ('user', 'colour',)
