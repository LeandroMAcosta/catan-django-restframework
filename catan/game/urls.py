from django.urls import path
from .views import GameViewSets, HexListViewSets

GameView_view = GameViewSets.as_view
HexListViewSets_view = HexListViewSets.as_view

urlpatterns = [
    path('<int:pk>/player/', GameView_view({
            'get': 'list_cards_and_resources'
        })
    ),
    path('<int:game_id>/board/', HexListViewSets_view({'get': 'list'})),
]
