from django.urls import path
from .views import GameViewSets

GameView_view = GameViewSets.as_view


urlpatterns = [
    path('<int:pk>/player/', GameView_view({'get': 'resources'})),
]
