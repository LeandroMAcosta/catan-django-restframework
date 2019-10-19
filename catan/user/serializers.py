from django.utils.translation import gettext as _
from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)
    # user = serializers.CharField(label=_("User"))

    def get_token(self, user):
        token = Token.objects.create(user=user)
        return str(token)

    def validate(self, attrs):
        username = attrs.get('user')
        password = attrs.get('password')
        print("\n\n\n\n\n\n")
        print(username, password)
        print("\n\n\n\n\n\n")
        attrs['user'] = username
        return attrs


    # def create(self, validated_data):
    #     password = validated_data.pop('password', None)
    #     username = validated_data['user']
    #     print("\n\n\n\n\nvalidated_data:\n")
    #     print(validated_data)
    #     print("\n\n\n\n\n\n")
    #     instance = User(username=username)
    #     if password is not None:
    #         instance.set_password(password)
    #     instance.save()
    #     return instance


class CustomAuthTokenSerializer(serializers.Serializer):
    user = serializers.CharField(label=_("User"))

    def __init__(self, *args, **kwargs):
        super(CustomAuthTokenSerializer, self).__init__(*args, **kwargs)
        self.fields['pass'] = serializers.CharField(
            label=_("Pass"),
            style={'input_type': 'password'},
            trim_whitespace=False
        )

    def validate(self, attrs):
        username = attrs.get('user')
        password = attrs.get('pass')

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
