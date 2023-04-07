from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework import test

from users.models import User


class SignUpViewTest(test.APITestCase):
    def setUp(self):
        self.client = test.APIClient()
        self.signup_url = reverse('signup')

    def test_success_signup(self):
        data = {'email': 'test@test.com', 'password': 'password123'}
        response = self.client.post(self.signup_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {'MESSAGE': 'SIGN_UP_SUCCESS'})
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@test.com')
        
    def test_failure_signup_exist_email(self):
        User(email='test0@test.com').save()
        data = {'email': 'test0@test.com', 'password': 'password123'}
        response = self.client.post(self.signup_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['code'], 400)
        self.assertEqual(
            response.json()['message'], 
            {'email': 'EMAIL_ALREADY_EXIST'}
        )

    def test_failure_signup_email_required(self):
        data = {'password': 'password123'}
        response = self.client.post(self.signup_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['code'], 400)
        self.assertEqual(
            response.json()['message'], 
            {'email': ['This field is required.']}
        )

    def test_failure_signup_password_required(self):
        data = {'email': 'test@test.com'}
        response = self.client.post(self.signup_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['code'], 400)
        self.assertEqual(
            response.json()['message'], 
            {'password': ['This field is required.']}
        )

    def test_failure_signup_email_password_required(self):
        data = {}
        response = self.client.post(self.signup_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['code'], 400)
        self.assertEqual(
            response.json()['message'], 
            {
                'email': ['This field is required.'], 
                'password': ['This field is required.']
            }
        )



class SignInViewTest(test.APITestCase):
    def setUp(self):
        self.client = test.APIClient()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            email='test@test.com', password='password123'
        )

    def test_success_signin(self):
        data = {'email': 'test@test.com', 'password': 'password123'}
        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'MESSAGE': 'SIGN_IN_SUCCESS'})
        self.assertIn('access_token', response.cookies)
        self.assertIn('refresh_token', response.cookies)

    def test_failure_signin_invalid_email(self):
        data = {'email': 'wrong@test.com', 'password': 'password123'}
        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['code'], 400)
        self.assertEqual(
            response.json()['message'], 
            {'non_field_errors': ['INVALID_EMAIL_OR_PASSWORD']})

    def test_failure_signin_invalid_password(self):
        data = {'email': 'test@test.com', 'password': 'wrong'}
        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['code'], 400)
        self.assertEqual(
            response.json()['message'], 
            {'non_field_errors': ['INVALID_EMAIL_OR_PASSWORD']})
        
    def test_failure_signin_email_required(self):
        data = {'password': 'password123'}
        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['code'], 400)
        self.assertEqual(
            response.json()['message'], 
            {'email': ['This field is required.']}
        )

    def test_failure_signin_password_required(self):
        data = {'email': 'test@test.com'}
        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['code'], 400)
        self.assertEqual(
            response.json()['message'], 
            {'password': ['This field is required.']}
        )

    def test_failure_signin_email_password_required(self):
        data = {}
        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['code'], 400)
        self.assertEqual(
            response.json()['message'], 
            {
                'email': ['This field is required.'], 
                'password': ['This field is required.']
            }
        )


class SignOutViewTest(test.APITestCase):
    def setUp(self):
        self.client = test.APIClient()
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user = User.objects.create_user(
            email='test@test.com', password='password123'
        )

    def test_success_logout(self):
        data = {'email': 'test@test.com', 'password': 'password123'}
        
        response = self.client.post(self.login_url, data)
        access_token = response.cookies['access_token']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'MESSAGE': 'SIGN_IN_SUCCESS'})
        self.assertIn('refresh_token', response.cookies)
        self.assertIn('access_token', response.cookies)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token.value}')
        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'MESSAGE': 'SIGN_OUT_SUCCESS'})
        self.assertEqual(BlacklistedToken.objects.count(), 2)
        
    def test_failure_logout_token_omission(self):
        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['code'], 401)
        self.assertEqual(
            response.json()['message'], 
            {
                'message': 'Authentication credentials were not provided.',
            }
        )