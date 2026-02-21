from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AdminNotification, PaymentClaim
from .serializers import AdminNotificationSerializer, PaymentClaimCreateSerializer, PaymentClaimListSerializer


class CreatePaymentClaimView(generics.CreateAPIView):
    serializer_class = PaymentClaimCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        claim = serializer.save()
        AdminNotification.objects.create(
            type=AdminNotification.Type.PAYMENT_CLAIM_SUBMITTED,
            reference_code=claim.reference_code,
            claim=claim,
        )


class MyPaymentClaimsView(generics.ListAPIView):
    serializer_class = PaymentClaimListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PaymentClaim.objects.filter(user=self.request.user).order_by("-created_at")


class AdminPaymentClaimsView(generics.ListAPIView):
    serializer_class = PaymentClaimListSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return PaymentClaim.objects.all().order_by("-created_at")


class AdminConfirmPaymentView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk, *args, **kwargs):
        claim = get_object_or_404(PaymentClaim, pk=pk)
        claim.status = PaymentClaim.Status.CONFIRMED
        claim.save(update_fields=["status", "updated_at"])
        AdminNotification.objects.create(
            type=AdminNotification.Type.PAYMENT_CONFIRMED,
            reference_code=claim.reference_code,
            claim=claim,
        )
        return Response(status=status.HTTP_200_OK)


class AdminRejectPaymentView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk, *args, **kwargs):
        claim = get_object_or_404(PaymentClaim, pk=pk)
        claim.status = PaymentClaim.Status.REJECTED
        claim.save(update_fields=["status", "updated_at"])
        AdminNotification.objects.create(
            type=AdminNotification.Type.PAYMENT_REJECTED,
            reference_code=claim.reference_code,
            claim=claim,
        )
        return Response(status=status.HTTP_200_OK)


class AdminNotificationsView(generics.ListAPIView):
    serializer_class = AdminNotificationSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return AdminNotification.objects.order_by("-created_at")


class AdminNotificationReadView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk, *args, **kwargs):
        notification = get_object_or_404(AdminNotification, pk=pk)
        notification.is_read = True
        notification.save(update_fields=["is_read"])
        return Response(status=status.HTTP_200_OK)

