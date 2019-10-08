from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('room/', include('lobby.urls')),
    path('users/login/', obtain_jwt_token),
    path('games/', include('game.urls')),
]
