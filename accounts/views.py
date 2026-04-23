from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView


from .models import UserProfile
from .serializers import ReferenceSerializer, RegisterSerializer
from .serializers import EmailOrUsernameTokenSerializer


User = get_user_model()


class AuthApiRootView(APIView):
    """GET /api/auth/ — lists auth routes (no trailing resource at this path otherwise 404)."""

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "detail": "ASVA auth API",
                "endpoints": {
                    "register": {"method": "POST", "url": "/api/auth/register"},
                },
            }
        )


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        profile = user.profile
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "reference_code": profile.reference_code,
            },
            status=status.HTTP_201_CREATED,
        )


class ReferenceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profile = UserProfile.objects.get(user=request.user)
        serializer = ReferenceSerializer({"reference_code": profile.reference_code})
        return Response(serializer.data)

class EmailOrUsernameTokenView(TokenObtainPairView):
    serializer_class = EmailOrUsernameTokenSerializer