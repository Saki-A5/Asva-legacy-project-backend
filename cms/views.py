from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import models

from .models import Content, Team, TeamJoinRequest, UserTeam, Event, Link, Internship, Document, Certificate
from .serializers import (
    ContentSerializer, TeamSerializer, TeamJoinRequestSerializer,
    EventSerializer, LinkSerializer, InternshipSerializer,
    DocumentSerializer, CertificateSerializer,
)


class PublicContentView(generics.RetrieveAPIView):
    queryset = Content.objects.filter(status=Content.Status.PUBLISHED)
    serializer_class = ContentSerializer
    lookup_field = "slug"
    permission_classes = [permissions.AllowAny]


class EventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # only return events that haven't passed yet
        return Event.objects.filter(date__gte=timezone.now()).order_by("date")


class TeamListView(generics.ListAPIView):
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Team.objects.all().order_by("name")


class TeamJoinRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = TeamJoinRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        team = serializer.validated_data["team"]

        # prevent duplicate requests
        if TeamJoinRequest.objects.filter(user=request.user, team=team).exists():
            return Response({"detail": "You already have a request for this team."}, status=status.HTTP_400_BAD_REQUEST)

        # prevent joining if already a member
        if UserTeam.objects.filter(user=request.user, team=team).exists():
            return Response({"detail": "You are already a member of this team."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        # return the user's own join requests
        requests = TeamJoinRequest.objects.filter(user=request.user).order_by("-created_at")
        serializer = TeamJoinRequestSerializer(requests, many=True)
        return Response(serializer.data)


class LinkListView(generics.ListAPIView):
    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_team_ids = UserTeam.objects.filter(user=self.request.user).values_list("team_id", flat=True)
        return Link.objects.filter(
            models.Q(team__isnull=True) | models.Q(team_id__in=user_team_ids)
        ).order_by("-created_at")


class InternshipListView(generics.ListAPIView):
    serializer_class = InternshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_team_ids = UserTeam.objects.filter(user=self.request.user).values_list("team_id", flat=True)
        return Internship.objects.filter(
            models.Q(team__isnull=True) | models.Q(team_id__in=user_team_ids),
            deadline__gte=timezone.now().date()
        ).order_by("deadline")


class DocumentListView(generics.ListAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_team_ids = UserTeam.objects.filter(user=self.request.user).values_list("team_id", flat=True)
        return Document.objects.filter(
            models.Q(team__isnull=True) | models.Q(team_id__in=user_team_ids)
        ).order_by("-created_at")


class CertificateListView(generics.ListAPIView):
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # return certificates issued to this user OR issued to everyone (null)
        return Certificate.objects.filter(
            models.Q(issued_to=self.request.user) | models.Q(issued_to__isnull=True)
        ).order_by("-issued_at")