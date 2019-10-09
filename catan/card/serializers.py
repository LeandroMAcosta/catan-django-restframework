from rest_framework import serializers
from card.models import Card


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ('id', 'player', 'card_type',)