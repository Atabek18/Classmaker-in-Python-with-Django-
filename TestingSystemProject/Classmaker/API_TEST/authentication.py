import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from UserResponse.models import UserRegisterModel
from django.conf import settings
from datetime import datetime, timedelta


class JWTAuthentication(BaseAuthentication):
    def __init__(self, request=None) -> None:
        self.request = request

    ALGORITHM = "HS256"
    TOKEN_TYPE = "Bearer"

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None, None
        try:
            token_type, token = auth_header.split()
            if token_type.lower() != self.TOKEN_TYPE.lower():
                raise AuthenticationFailed("Invalid token type")

            decoded_payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[self.ALGORITHM]
            )
            user_id = decoded_payload.get("user_id")
            if user_id:
                try:
                    user = UserRegisterModel.objects.get(id=user_id)
                    return user, True
                except UserRegisterModel.DoesNotExist:
                    raise AuthenticationFailed("User not found")
            else:
                raise AuthenticationFailed("Invalid user_id in token")

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

    def authenticate_header(self):
        return self.TOKEN_TYPE

    def generate_token(self, payload):
        expiration_time = datetime.utcnow() + timedelta(minutes=15)
        payload["exp"] = expiration_time
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    def generate_student_token(self, user: UserRegisterModel):
        payload = {
            "quiz_id": user.assign.slug_field,
            "user_id": user.id,
            "first_name": user.name,
            "last_name": user.surname,
            "email": user.email,
            "season_type": user.season_type,
            "phone_number": str(user.phone_number),
            "season_number": user.season_number,
        }
        return self.generate_token(payload)

    def generate_quiz_token(self, quiz_id):
        payload = {
            "quiz_id": quiz_id,
        }
        return self.generate_token(payload)

    def update_token(self):
        user, _ = self.authenticate(self.request)
        access_token_payload = {
            "user_id": user.id,
        }
        new_access_token = self.generate_token(access_token_payload)
        return new_access_token

    def decode_token(self, token):
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[self.ALGORITHM]
        )
        return decoded_token

    def get_student(self):
        request = self.request
        user, _ = self.authenticate(request)
        return user

    def get_anything_from_token(self, key: str, keys: list[str] = None):
        auth_header = self.request.headers.get("Authorization")
        token_type, token = auth_header.split()
        decoded_info = self.decode_token(token)
        return decoded_info[key]
