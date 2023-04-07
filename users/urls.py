from django.urls import path

from users.views import SignUpView, SignInView, SignOutView


urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('login', SignInView.as_view(), name='login'),
    path('logout', SignOutView.as_view(), name='logout'),
]