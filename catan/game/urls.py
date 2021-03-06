from django.urls import path

from .views import GameViewSets, HexListViewSets

GameView = GameViewSets.as_view
HexView = HexListViewSets.as_view

urlpatterns = [
    path(
        '<int:game>/player/',
        GameView({
            'get': 'list_cards_and_resources'
        }),
        name='player-info'
    ),
    path(
        '<int:game>/player/actions/',
        GameView({
            'post': 'action'
        }),
        name='player-action'
    ),
    path('<int:game>/board/', HexView({
        'get': 'list'
    })),
]
