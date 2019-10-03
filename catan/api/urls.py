from django.urls import path, include

urlpatterns = [
    path('rooms/<id>', include('lobby.urls')),
]
