from django.urls import path
from .views import CustomObtainAuthToken, UserSignup

obtain_auth_token = CustomObtainAuthToken.as_view()

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('signup/', UserSignup.as_view({'post': 'create'}), name='signup'),
]
