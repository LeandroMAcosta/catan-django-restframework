from django.urls import path, include

urlpatterns = [
    path('room/', include('lobby.urls')),
    path('games/', include('game.urls')),
    path('users/', include('user.urls')),
]
