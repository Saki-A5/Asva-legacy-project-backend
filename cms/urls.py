from django.urls import path

from .views import (
    PublicContentView, EventListView, TeamListView,
    TeamJoinRequestView, LinkListView, InternshipListView,
    DocumentListView, CertificateListView,
)

urlpatterns = [
    path("content/<slug:slug>", PublicContentView.as_view(), name="cms-content-detail"),
    path("events", EventListView.as_view(), name="cms-events"),
    path("teams", TeamListView.as_view(), name="cms-teams"),
    path("teams/join", TeamJoinRequestView.as_view(), name="cms-team-join"),
    path("links", LinkListView.as_view(), name="cms-links"),
    path("internships", InternshipListView.as_view(), name="cms-internships"),
    path("documents", DocumentListView.as_view(), name="cms-documents"),
    path("certificates", CertificateListView.as_view(), name="cms-certificates"),
]