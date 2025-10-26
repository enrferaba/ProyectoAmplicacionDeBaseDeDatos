from django.urls import path

from .views import LoginView, LogoutView, OTPRequestView, OTPVerifyView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('otp/request', OTPRequestView.as_view(), name='otp-request'),
    path('otp/verify', OTPVerifyView.as_view(), name='otp-verify'),
]
