from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils import timezone


class Content(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"

    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255)
    body = models.TextField()
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.DRAFT, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TeamJoinRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="team_requests")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="join_requests")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "team")

    def __str__(self):
        return f"{self.user.username} → {self.team.name} ({self.status})"


class UserTeam(models.Model):
    """Approved team memberships."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="teams")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "team")

    def __str__(self):
        return f"{self.user.username} — {self.team.name}"


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField()
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def is_expired(self):
        return self.date < timezone.now()


class Link(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(blank=True)
    # null = visible to all members
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="links")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Internship(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    apply_url = models.URLField()
    deadline = models.DateField()
    # null = visible to all members
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="internships")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} — {self.company}"

    @property
    def is_expired(self):
        return self.deadline < timezone.now().date()


class Document(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(blank=True)
    # null = visible to all members
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="documents")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Certificate(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    issued_at = models.DateField()
    # null = issued to ALL members
    issued_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="certificates",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        target = self.issued_to.username if self.issued_to else "All Members"
        return f"{self.title} → {target}"