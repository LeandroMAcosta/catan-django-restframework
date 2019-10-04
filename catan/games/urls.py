from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from games import views

urlpatterns = [
    path('<int:game_id>/board', views.HexList.as_view({'get': 'list'})),
]
