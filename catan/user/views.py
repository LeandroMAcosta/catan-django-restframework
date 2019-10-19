from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import CustomAuthTokenSerializer


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
