from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from .scripts import normalize_phone

User = get_user_model()


class AuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        email = username
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def has_perm(self, user, perm, obj=None):
        return user.is_staff
