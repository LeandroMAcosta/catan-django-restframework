from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Room


class RoomsView(APIView):
    # The username and password of your superuser
    # This should be in users
    # This function retorn the superuser with a token
    def login(self):
        user = authenticate(username='Lucas', password='Aguantejmkmu1239')
        token, _ = Token.objects.get_or_create(user=user)
        return (user, token)

    def get(self, request):
        rooms = Room.objects.all()
        list_rooms = [room.id for room in rooms]
        return Response(list_rooms)

    # 403 Forbidden -> PermissionDenied
    # 401 Unauthorized -> NotAuthenticated
    def put(self, request, id):
        rooms = Room.objects.all()
        content = None
        for r in rooms:
            if id == rooms.id:
                content = r
                break
        if content is None:
            content = {'error': 'The room does not exist'}
        else:
            # Here join lobby
            pass
        return Response(content)
