from django.urls import path
from . import views


urlpatterns = [
    path('<id>/', views.ListRoomsViewSets.as_view(put='join_room')),
    path('', views.ListRoomsViewSets.as_view(get ='list')),
]