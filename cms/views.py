import hmac
import json
from hashlib import sha256

import requests
from django.conf import settings
from django.http import HttpResponseForbidden
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Content
from .serializers import ContentSerializer


class PublicContentView(generics.RetrieveAPIView):
    queryset = Content.objects.filter(status=Content.Status.PUBLISHED)
    serializer_class = ContentSerializer
    lookup_field = "slug"
    permission_classes = [permissions.AllowAny]


class NextjsWebhookView(APIView):
    """
    Webhook endpoint called by Django when content is published to trigger Next.js revalidation.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        secret = settings.NEXTJS_WEBHOOK_SECRET
        received_signature = request.headers.get("X-ASVA-Signature", "")

        computed = hmac.new(secret.encode(), request.body, sha256).hexdigest()
        if not hmac.compare_digest(received_signature, computed):
            return HttpResponseForbidden("Invalid signature")

        payload = json.loads(request.body.decode("utf-8"))
        path = payload.get("path", "/")

        requests.post(
            settings.NEXTJS_REVALIDATE_URL,
            json={"path": path, "secret": secret},
            timeout=5,
        )
        return Response(status=status.HTTP_200_OK)

