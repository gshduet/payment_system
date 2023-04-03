from django.contrib.auth import authenticate
from django.utils.timezone import now
from rest_framework import serializers

from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
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
    
    def validate(self, data):
        email = data['email']
        password = data['password']
        
        user = authenticate(email=email, password=password)

        if user is not None:
            user.last_login = now()
            user.save()
            
            token = RefreshToken.for_user(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            data = {
                'user': user,
                'refresh_token': refresh_token,
                'access_token': access_token
            }

            return data

        else:
            raise serializers.ValidationError('INVALID_EMAIL_OR_PASSWORD')