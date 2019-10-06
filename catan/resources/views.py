from django.views import View
from django.shortcuts import render


# Create your views here.
from .models import Resources


class ResourcesView(APIView):
    def get(self, request, plyr):
        resource = Resources.objects.filter(owner_player=plyr)
        list_resource = [resources.id for resources in resource]
        return Response(list_resource)
