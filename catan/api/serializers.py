from django.utils.translation import gettext as _
from rest_framework import serializers
from django.contrib.auth import authenticate


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
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
