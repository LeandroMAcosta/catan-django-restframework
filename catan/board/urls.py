from django.urls import path

from .views import HexListViewSets

HexListViewSets_view = HexListViewSets.as_view

urlpatterns = [
    path('<int:game_id>/board/', HexListViewSets_view({
        'get': 'list'
    })),
]
