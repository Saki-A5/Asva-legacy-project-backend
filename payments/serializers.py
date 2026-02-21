from __future__ import annotations

from rest_framework import serializers

from .models import AdminNotification, PaymentClaim


class PaymentClaimCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentClaim
        fields = ["amount"]

    def create(self, validated_data):
        user = self.context["request"].user
        profile = user.profile
        return PaymentClaim.objects.create(
            user=user,
            reference_code=profile.reference_code,
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

