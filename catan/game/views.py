from django.shortcuts import render


class GameViewSets(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GameSerializer
