from django.urls import path, include

urlpatterns = [
    path('users/login/', obtain_auth_token),
    path('rooms/', include('lobby.urls')),
    path('games/', include('game.urls')),
    path('users/', include('user.urls')),
]
