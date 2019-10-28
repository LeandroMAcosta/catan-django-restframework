from django.urls import path

from .views import GameViewSets

GameViewSets_view = GameViewSets.as_view

urlpatterns = [
    path('<int:pk>/board/', GameViewSets_view({
        'get': 'list'
    })),
]
