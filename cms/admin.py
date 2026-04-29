from django.contrib import admin

from .models import (
    Content, Team, TeamJoinRequest, UserTeam,
    Event, Link, Internship, Document, Certificate
)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "status", "updated_at")
    list_filter = ("status", "updated_at")
    search_fields = ("title", "slug")


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    search_fields = ["name"]


@admin.register(TeamJoinRequest)
class TeamJoinRequestAdmin(admin.ModelAdmin):
    list_display = ["user", "team", "status", "created_at"]
    list_filter = ["status", "team"]
    actions = ["approve", "reject"]

    def approve(self, request, queryset):
        for join_request in queryset.filter(status=TeamJoinRequest.Status.PENDING):
            join_request.status = TeamJoinRequest.Status.APPROVED
            join_request.save()
            UserTeam.objects.get_or_create(user=join_request.user, team=join_request.team)
    approve.short_description = "Approve selected requests"

    def reject(self, request, queryset):
        queryset.filter(status=TeamJoinRequest.Status.PENDING).update(
            status=TeamJoinRequest.Status.REJECTED
        )
    reject.short_description = "Reject selected requests"


@admin.register(UserTeam)
class UserTeamAdmin(admin.ModelAdmin):
    list_display = ["user", "team", "joined_at"]
    list_filter = ["team"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "date", "location", "created_at"]
    list_filter = ["date"]
    search_fields = ["title"]


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ["title", "url", "team", "created_at"]
    list_filter = ["team"]
    search_fields = ["title"]


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ["title", "company", "deadline", "team", "created_at"]
    list_filter = ["team", "deadline"]
    search_fields = ["title", "company"]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["title", "url", "team", "created_at"]
    list_filter = ["team"]
    search_fields = ["title"]


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ["title", "issued_to", "issued_at", "created_at"]
    list_filter = ["issued_at"]
    search_fields = ["title", "issued_to__username"]