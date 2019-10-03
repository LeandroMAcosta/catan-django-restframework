from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Room

class RoomsView(APIView):
    def get(self, request):
        print("ghola, llegue aca bro")
        rooms = Room.objects.all()
        return Response({"rooms": rooms})



"""
def join_room(self, request):

        print(request)
        # request.user

        # if(len(this.players) < this.max_players):
        #     this.players.append(player)
"""