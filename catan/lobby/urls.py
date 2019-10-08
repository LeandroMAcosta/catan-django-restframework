from django.urls import path
from .views import RoomsView


urlpatterns = [
    path('', RoomsView.as_view()),
    path('<int:room_id>/', RoomsView.as_view()),
]
