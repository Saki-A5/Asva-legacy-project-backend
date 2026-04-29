from __future__ import annotations

from rest_framework import serializers

from .models import Content, Team, TeamJoinRequest, Event, Link, Internship, Document, Certificate


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ["id", "slug", "title", "body", "status", "updated_at", "created_at"]


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name", "description", "created_at"]


class TeamJoinRequestSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source="team.name", read_only=True)

    class Meta:
        model = TeamJoinRequest
        fields = ["id", "team", "team_name", "status", "created_at"]
        read_only_fields = ["status", "created_at"]


class EventSerializer(serializers.ModelSerializer):
    is_expired = serializers.BooleanField(read_only=True)

    class Meta:
        model = Event
        fields = ["id", "title", "description", "location", "date", "image_url", "is_expired", "created_at"]


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ["id", "title", "url", "description", "team", "created_at"]


class InternshipSerializer(serializers.ModelSerializer):
    is_expired = serializers.BooleanField(read_only=True)

    class Meta:
        model = Internship
        fields = ["id", "title", "company", "location", "description", "apply_url", "deadline", "is_expired", "team", "created_at"]


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "title", "url", "description", "team", "created_at"]


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ["id", "title", "description", "url", "issued_at", "issued_to", "created_at"]