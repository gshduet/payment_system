from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.serializers import UserSerializer


class SignUpView(APIView):

    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        """
        회원가입 API
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({'MESSAGE': 'SIGN_UP_SUCCESS'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):

    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        """
        로그인 API
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            response = Response(data={'MESSAGE': 'SIGN_IN_SUCCESS'}, status=status.HTTP_200_OK)

            response.set_cookie(
                key='access_token', value=serializer.validated_data['access_token'],
                httponly=True
            )
            response.set_cookie(
                key='refresh_token', value=serializer.validated_data['refresh_token'],
                httponly=True
            )

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignOutView(APIView):

    authentication_classes = [JWTAuthentication]

    def post(self, request):
        """
        로그아웃 API
        """
        response = Response({'MESSAGE': 'SIGN_OUT_SUCCESS'},
                            status=status.HTTP_200_OK)

        response.delete_cookie('access_token')

        # refresh_token = RefreshToken(request.META.get('refresh_token'))
        # access_token = RefreshToken(request.META.get('access_token'))
        # refresh_token.blacklist()
        # access_token.blacklist()

        return response
