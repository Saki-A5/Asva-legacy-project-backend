from django.contrib import admin

from .models import AdminNotification, PaymentClaim


@admin.register(PaymentClaim)
class PaymentClaimAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "reference_code", "amount", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("reference_code", "user__username", "user__email")
    actions = ["mark_confirmed", "mark_rejected"]

    @admin.action(description="Mark selected claims as confirmed")
    def mark_confirmed(self, request, queryset):
        for claim in queryset:
            claim.status = PaymentClaim.Status.CONFIRMED
            claim.save(update_fields=["status", "updated_at"])
            AdminNotification.objects.create(
                type=AdminNotification.Type.PAYMENT_CONFIRMED,
                reference_code=claim.reference_code,
                claim=claim,
            )

    @admin.action(description="Mark selected claims as rejected")
    def mark_rejected(self, request, queryset):
        for claim in queryset:
            claim.status = PaymentClaim.Status.REJECTED
            claim.save(update_fields=["status", "updated_at"])
            AdminNotification.objects.create(
                type=AdminNotification.Type.PAYMENT_REJECTED,
                reference_code=claim.reference_code,
                claim=claim,
            )


@admin.register(AdminNotification)
class AdminNotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "reference_code", "claim", "is_read", "created_at")
    list_filter = ("type", "is_read", "created_at")
    search_fields = ("reference_code",)

