from rest_framework import serializers
from snippets.models import Snippet

class RoomSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(style={'base_template': 'textarea.html'})
    owner = serializers.CharField(max_length=100) #Change to USERNAME
    #needs to be a relation between tables 
    #players = [] #Arrays of USERNAMEs
    max_players = serializers.IntegerField(default=4)


    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)
    

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.max_players = validated_data.get('max_players', instance.max_players)
        instance.save()
        return instance
