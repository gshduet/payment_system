from django.utils.timezone import now
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserSignupSerializer, UserSigninSerializer


class SignUpView(APIView):

    permission_classes = [AllowAny]
    serializer_class = UserSignupSerializer

    def post(self, request):
        """
        회원가입 API
        클라이언트로부터 다음과 같은 데이터가 담긴 요청을 받습니다.
        {
            'email': 'test@test.com',
            'password': 'password123',
        }
        무결성 검사 통과 시 성공적으로 계정이 생성된 뒤 
        201 상태코드와 'MESSAGE': 'SIGN_UP_SUCCESS' 문구를 클라이언트에게 반환합니다.

        다음과 같은 경우에 계정 생성에 실패합니다.
        1. 이미 존재하는 이메일을 입력하여 회원가입을 시도할 경우
        2. 이메일 혹은 패스워드를 누락하여 요청할 경우
        """
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'MESSAGE': 'SIGN_UP_SUCCESS'}, status=status.HTTP_201_CREATED)


class SignInView(APIView):

    permission_classes = [AllowAny]
    serializer_class = UserSigninSerializer

    def post(self, request):
        """
        로그인 API
        클라이언트로부터 다음과 같은 데이터가 담긴 요청을 받습니다.
        {
            'email': 'test@test.com',
            'password': 'password123',
        }
        무결성 검사 통과 시 마지막 로그인 시간을 최신화 하고 
        해당 이메일 계정의 UUID를 기반으로 JWT(refresh_token, access_token)를 생성하여 쿠키에 저장합니다.
        200 상태코드와 'MESSAGE': 'SIGN_IN_SUCCESS' 문구를 쿠키와 함께 클라이언트에게 반환합니다.

        이후 인증을 필요로 하는 요청마다 요청헤더의 Authorization Header 항목을 확인하고
        헤더에 access_token이 존재하지 않거나 토큰의 유효기간 만료, 변조가 확인될 경우
        401 상태코드와 'message': 'Authentication credentials were not provided.'를 반환합니다.
        토큰이 아직 유효하거나 변조되지 않을 경우 정상적인 요청으로 받아들여 클라이언트가 원하는 행위를 진행합니다.

        이 과정은 StatelessUserAuthentication을 바탕으로 구현하였음으로 Django의 세션프레임워크를 사용하지 않습니다.
        그러므로 인증 과정에서 서버와의 통신 없이 진행됩니다.
        """
        serializer = self.serializer_class(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.last_login = now()
        user.save()

        response = Response({'MESSAGE': 'SIGN_IN_SUCCESS'}, status=status.HTTP_200_OK)

        response.set_cookie(
            key='access_token', value=serializer.validated_data['access_token'],
            httponly=True
        )
        response.set_cookie(
            key='refresh_token', value=serializer.validated_data['refresh_token'],
            httponly=True
        )
        
        return response


class SignOutView(APIView):

    def post(self, request):
        """
        로그아웃 API
        클라이언트로부터 로그아웃 요청을 받을 경우 쿠키에 저장된 refresh_token, access_token을 제거합니다.
        이후 해당 유저에게 발급했던 refresh_token을 blacklist에 등록하여 무효화합니다.

        만약 요청헤더의 Authorization Header에 access_token이 존재하지 않거나 토큰의 유효기간 만료, 변조가 확인될 경우
        401 상태코드와 'message': 'Authentication credentials were not provided.'를 반환합니다.
        토큰이 아직 유효하거나 변조되지 않을 경우 정상적인 요청으로 받아들여 클라이언트가 원하는 행위를 진행합니다.

        성공적으로 로그아웃이 완료될 경우 유저에게 발급했던 refresh_token과 access_token은 사용할 수 없게 됩니다.
        """
        response = Response({'MESSAGE': 'SIGN_OUT_SUCCESS'}, status=status.HTTP_200_OK)

        refresh_token = RefreshToken(request.COOKIES['refresh_token'])
        refresh_token.blacklist()
        response.delete_cookie('refresh_token')
        response.delete_cookie('access_token')

        return response