from django.urls import path

from .views import AuthApiRootView, RegisterView


urlpatterns = [
    path("", AuthApiRootView.as_view(), name="auth-api-root"),
    path("register", RegisterView.as_view(), name="register"),
]

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import AuthApiRootView, RegisterView, EmailOrUsernameTokenView

urlpatterns = [
    path("", AuthApiRootView.as_view(), name="auth-api-root"),
    path("register", RegisterView.as_view(), name="register"),
    path("login", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path("token", EmailOrUsernameTokenView.as_view(), name="token_obtain_pair"),
]
