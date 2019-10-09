from rest_framework import serializers
from resource.models import Resource


class ResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resource
        # fields = ('resource', 'owner',)
        fields = "__all__"
