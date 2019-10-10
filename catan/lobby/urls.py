from django.urls import path
from .views import RoomsView


urlpatterns = [
    path('', RoomsView.as_view({'get': 'list'})),
    path('<int:room_id>/', RoomsView.as_view({'put': 'update'})),
]
