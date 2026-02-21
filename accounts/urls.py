from django.urls import path

from .views import ReferenceView, RegisterView


urlpatterns = [
    path("register", RegisterView.as_view(), name="register"),
    path("me/reference", ReferenceView.as_view(), name="me-reference"),
]

