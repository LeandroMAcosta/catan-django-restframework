from django.urls import path, include
from .views import CustomObtainAuthToken

obtain_auth_token = CustomObtainAuthToken.as_view()

urlpatterns = [
    path('users/login/', obtain_auth_token),
    path('room/', include('lobby.urls')),
    path('games/', include('game.urls')),
]
