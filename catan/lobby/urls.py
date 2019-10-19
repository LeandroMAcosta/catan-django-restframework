from django.urls import path
from .views import RoomsView


urlpatterns = [
    path('', RoomsView.as_view({
        'post': 'create',
        'get': 'list',
        })),
    path('<int:room_id>/', RoomsView.as_view({'put': 'join'})),
]
