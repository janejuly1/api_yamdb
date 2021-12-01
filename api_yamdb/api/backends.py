from rest_framework.exceptions import PermissionDenied
from reviews.models import User, ConfirmationCode


class ConfirmationCodeAuthBackend:
    def authenticate(self, request, username=None, confirmation_code=None):
        try:
            code = ConfirmationCode.objects.get(
                user__username=username,
                code=confirmation_code
            )
        except ConfirmationCode.DoesNotExist:
            raise PermissionDenied('user not found')

        return code.user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

