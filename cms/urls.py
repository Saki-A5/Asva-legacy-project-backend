from django.urls import path

from .views import NextjsWebhookView, PublicContentView


urlpatterns = [
    path("content/<slug:slug>", PublicContentView.as_view(), name="cms-content-detail"),
    path("webhook/revalidate", NextjsWebhookView.as_view(), name="nextjs-webhook-revalidate"),
]

