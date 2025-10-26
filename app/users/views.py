from django.conf import settings
from django.contrib.auth import login, logout
from django.http import HttpRequest
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.otp import otp_service
from core.rate_limit import login_rate_limiter
from .serializers import LoginSerializer, OTPRequestSerializer, OTPVerifySerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: HttpRequest):
        client_ip = request.META.get('REMOTE_ADDR', 'unknown')
        limiter = login_rate_limiter.allow(
            identifier=f"ip:{client_ip}",
            limit=settings.RATE_LIMIT_LOGIN,
            window=settings.RATE_LIMIT_LOGIN_WINDOW,
        )
        if not limiter.allowed:
            return Response({'detail': 'Too many login attempts. Try again later.'}, status=429)
        username = request.data.get('username', '')
        limiter_user = login_rate_limiter.allow(
            identifier=f"user:{username}",
            limit=settings.RATE_LIMIT_LOGIN,
            window=settings.RATE_LIMIT_LOGIN_WINDOW,
        )
        if not limiter_user.allowed:
            return Response({'detail': 'Too many login attempts for this user.'}, status=429)
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({'message': 'Login successful.', 'user_id': user.id})


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: HttpRequest):
        logout(request)
        return Response({'message': 'Logout successful.'})


class OTPRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: HttpRequest):
        serializer = OTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data['user_id']
        try:
            otp = otp_service.generate(user_id)
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=429)
        return Response({'message': 'OTP generated successfully.', 'ttl': otp.ttl, 'code': otp.code})


class OTPVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: HttpRequest):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data['user_id']
        code = serializer.validated_data['code']
        try:
            success = otp_service.verify(user_id, code)
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=429)
        if not success:
            return Response({'detail': 'Invalid or expired OTP.'}, status=400)
        return Response({'message': 'OTP verified successfully.'})
