from django.urls import path
from .views import RoomsView


urlpatterns = [
    path('<int:pk>/', RoomsView.as_view({
        'get': 'list_room',
        'put': 'join',
        'patch': 'start_game',
        'delete': 'cancel_lobby'
    })),
    path('', RoomsView.as_view({
        'post': 'create',
        'get': 'list_rooms',
    })),
]
