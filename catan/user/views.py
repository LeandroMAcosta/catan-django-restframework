from django.db import IntegrityError as AlredyExist

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from .serializers import CustomAuthTokenSerializer, UserSerializerWithToken
from .models import User

from .exceptions import UserOrPasswordEmpty


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer


class UserSignup(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializerWithToken
    queryset = User.objects.all()

    def create(self, request):
        try:
            username = request.data['user']
            password = request.data['pass']
            if username and password:
                instance = User(username=username)
                instance.set_password(password)
                instance.save()
                return Response(
                    "User created.",
                    status=status.HTTP_201_CREATED
                )
            raise UserOrPasswordEmpty

        except AlredyExist:
            return Response(
                "User alredy exist.",
                status=status.HTTP_409_CONFLICT
            )
        except UserOrPasswordEmpty:
            return Response(
                "Must include 'user' and 'pass'",
                status=status.HTTP_409_CONFLICT
            )
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
