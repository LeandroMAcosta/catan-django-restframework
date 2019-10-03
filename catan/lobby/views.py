from rest_framework.views import APIView
from rest_framework.response import Response
from lobby.models import Room
from rest_framework import authentication

class ListRoomsViewSets(APIView):

    """
    Requires token authentication
    """
    authentication_classes = [authentication.TokenAuthentication]

    
    def list(self, request):
        """
        Return a list of all Lobbies.
        """
        lobbies = [room.name for room in Room.objects.all()]
        return Response(lobbies)
    
    def join_room(self, request):

        print(request)
        # request.user

        # if(len(this.players) < this.max_players):
        #     this.players.append(player)