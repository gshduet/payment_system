from django.middleware import csrf

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt import tokens


class JWTAccessToken(tokens.BlacklistMixin, tokens.AccessToken):
    pass


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        csrf_secret = csrf._get_new_csrf_string()

        token['email'] = user.email
        token['CSRF_TOKEN'] = csrf._mask_cipher_secret(csrf_secret)

        return token