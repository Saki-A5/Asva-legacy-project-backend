from __future__ import annotations

from django.conf import settings
from django.db import models


class PaymentClaim(models.Model):
    class Status(models.TextChoices):
        PENDING_REVIEW = "PENDING_REVIEW", "Pending review"
        CONFIRMED = "CONFIRMED", "Confirmed"
        REJECTED = "REJECTED", "Rejected"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payment_claims")
    reference_code = models.CharField(max_length=9, db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.PENDING_REVIEW, db_index=True)
    admin_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.reference_code} - {self.amount} ({self.status})"


class AdminNotification(models.Model):
    class Type(models.TextChoices):
        PAYMENT_CLAIM_SUBMITTED = "PAYMENT_CLAIM_SUBMITTED", "Payment claim submitted"
        PAYMENT_CONFIRMED = "PAYMENT_CONFIRMED", "Payment confirmed"
        PAYMENT_REJECTED = "PAYMENT_REJECTED", "Payment rejected"

    type = models.CharField(max_length=64, choices=Type.choices)
    reference_code = models.CharField(max_length=9, db_index=True)
    claim = models.ForeignKey(PaymentClaim, on_delete=models.CASCADE, related_name="notifications")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.type} - {self.reference_code}"

