from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import UserProfile
from .utils import generate_reference_code
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        UserProfile.objects.create(user=user, reference_code=generate_reference_code())

        return user


class ReferenceSerializer(serializers.Serializer):
    reference_code = serializers.CharField(read_only=True)

class EmailOrUsernameTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        
        login_input = attrs.get('username')
        if '@' in login_input:
            try:
                user = User.objects.get(email=login_input)
                attrs['username'] = user.username
            except User.DoesNotExist:
                pass
        return super().validate(attrs)
         