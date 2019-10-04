from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Room

class RoomsView(APIView):

    def get(self, request):
        rooms = Room.objects.all()
        list_rooms  = [room.id for room in rooms]
        return Response(list_rooms)

    def put(self, request, id):
        return Response([])


