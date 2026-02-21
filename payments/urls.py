from django.urls import path

from .views import (
    AdminConfirmPaymentView,
    AdminNotificationReadView,
    AdminNotificationsView,
    AdminPaymentClaimsView,
    AdminRejectPaymentView,
    CreatePaymentClaimView,
    MyPaymentClaimsView,
)


urlpatterns = [
    path("claim", CreatePaymentClaimView.as_view(), name="payment-claim"),
    path("claims/me", MyPaymentClaimsView.as_view(), name="payment-claims-me"),
    path("admin/payment-claims", AdminPaymentClaimsView.as_view(), name="admin-payment-claims"),
    path("admin/payment-claims/<int:pk>/confirm", AdminConfirmPaymentView.as_view(), name="admin-payment-confirm"),
    path("admin/payment-claims/<int:pk>/reject", AdminRejectPaymentView.as_view(), name="admin-payment-reject"),
    path("admin/notifications", AdminNotificationsView.as_view(), name="admin-notifications"),
    path("admin/notifications/<int:pk>/read", AdminNotificationReadView.as_view(), name="admin-notification-read"),
]

