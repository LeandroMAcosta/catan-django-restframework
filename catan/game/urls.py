from django.urls import path

from .views import GameViewSets

GameView = GameViewSets.as_view

urlpatterns = [
    path('<int:pk>/player/', GameView({
            'get': 'list_cards_and_resources'
        }), name='player-info'
    ),
    path('<int:pk>/player/actions/', GameView({
            'post': 'action'
        }), name='player-action'
    ),
    path('<int:pk>/board/', GameView({
        'get': 'list'
    })),
]
