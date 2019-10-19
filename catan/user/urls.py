from django.urls import path
from .views import CustomObtainAuthToken

obtain_auth_token = CustomObtainAuthToken.as_view()

urlpatterns = [
    path('login/', obtain_auth_token),
]
