# myapp/permissions.py

from rest_framework import permissions
from rest_framework.authentication import get_authorization_header
from .authentication import JWTAuthentication
from UserResponse.models import UserRegisterModel


class IsJWTTokenProvided(permissions.BasePermission):
    def has_permission(self, request, view):
        authorization_header = get_authorization_header(request).decode("utf-8")
        if not authorization_header or not authorization_header.startswith("Bearer "):
            return False
        token = authorization_header.split("Bearer ")[1].strip()
        try:
            decoded_user = JWTAuthentication().decode_token(token)
            return UserRegisterModel.objects.filter(id=decoded_user["user_id"]).exists()
        except Exception:
            return False
