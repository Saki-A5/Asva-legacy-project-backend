from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import AuthApiRootView, RegisterView, EmailOrUsernameTokenView, LogoutView

urlpatterns = [
    path("", AuthApiRootView.as_view(), name="auth-api-root"),
    path("register", RegisterView.as_view(), name="register"),
    path("login", EmailOrUsernameTokenView.as_view(), name="login"),
    path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout", LogoutView.as_view(), name="logout"),
]