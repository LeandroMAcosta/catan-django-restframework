from django.urls import path, include

urlpatterns = [
    path('rooms/', include('lobby.urls')),
    path('games/', include('game.urls')),
    path('users/', include('user.urls')),
]
