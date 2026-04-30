from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import AdminNotification, PaymentClaim

User = get_user_model()


class PaymentClaimCreateSerializer(serializers.ModelSerializer):
    reference_code = serializers.CharField(max_length=16)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = PaymentClaim
        fields = ["reference_code", "email", "amount"]

    def validate(self, attrs):
        reference_code = attrs.get("reference_code")
        email = attrs.get("email")

        # find user by reference code
        try:
            from accounts.models import UserProfile
            profile = UserProfile.objects.select_related("user").get(reference_code=reference_code)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError({"reference_code": "Invalid reference code."})

        # check email matches
        if profile.user.email.lower() != email.lower():
            raise serializers.ValidationError({"email": "Email does not match this reference code."})

        # prevent duplicate claims
        if PaymentClaim.objects.filter(reference_code=reference_code).exists():
            raise serializers.ValidationError({"reference_code": "A claim has already been submitted for this reference code."})

        attrs["user"] = profile.user
        return attrs

    def create(self, validated_data):
        validated_data.pop("email")
        user = validated_data.pop("user")
        return PaymentClaim.objects.create(
            user=user,
            status=PaymentClaim.Status.PENDING_REVIEW,
            **validated_data,
        )


class PaymentClaimListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentClaim
        fields = ["id", "reference_code", "amount", "status", "admin_note", "created_at", "updated_at"]


class AdminNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminNotification
        fields = ["id", "type", "reference_code", "claim", "is_read", "created_at"]