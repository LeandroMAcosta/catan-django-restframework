from django.urls import path
from .views import RoomsView


urlpatterns = [
    path('', RoomsView.as_view({
        'post': 'create',
        'get': 'list',
    })),
    path('<int:pk>/', RoomsView.as_view({
        'put': 'join',
        'patch': 'start_game',
        'delete': 'cancel_lobby'
    })),
]
