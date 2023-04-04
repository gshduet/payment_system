from django.contrib.auth import authenticate
from django.db import utils
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class UserSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=127)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
            )
        return user

class UserSigninSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=127)
    password = serializers.CharField(write_only=True)
    user = serializers.SerializerMethodField()
    access_token = serializers.SerializerMethodField()
    refresh_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate(self, data):
        email = data['email']
        password = data['password']
        
        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if user is None:
            raise serializers.ValidationError(detail=_('INVALID_EMAIL_OR_PASSWORD'), code='AUTHORIZATION')

        token = RefreshToken.for_user(user)

        data['user'] = user
        data['refresh_token'] = str(token)
        data['access_token'] = str(token.access_token)

        return data