from rest_framework import serializers


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ()
