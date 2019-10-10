from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('users/login/', obtain_jwt_token),
    path('room/', include('lobby.urls')),
    path('games/', include('game.urls')),
]
