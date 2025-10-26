from django.contrib.auth import authenticate
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get('request'),
            username=attrs['username'],
            password=attrs['password'],
        )
        if not user:
            raise serializers.ValidationError('Invalid credentials.')
        attrs['user'] = user
        return attrs


class OTPRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class OTPVerifySerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)
