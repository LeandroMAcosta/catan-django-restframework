from django.urls import path, include

urlpatterns = [
    path('room/', include('lobby.urls')),
]
