from __future__ import annotations

from rest_framework import serializers

from .models import Content


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ["id", "slug", "title", "body", "status", "updated_at", "created_at"]

