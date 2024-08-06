from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from users.models import User
from rest_framework_simplejwt.settings import api_settings

class UUIDJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user_model = User
        user_id = validated_token.get(api_settings.USER_ID_FIELD)
        if user_id is None:
            raise TokenError(
                'Token contained no recognizable user identification field.'
            )
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            raise TokenError('User not found.')
