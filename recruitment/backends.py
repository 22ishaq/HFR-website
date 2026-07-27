from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q


class FlexibleLoginBackend(ModelBackend):
    """Log in with username, email, or the display name chosen at onboarding."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        try:
            user = User.objects.get(
                Q(username__iexact=username)
                | Q(email__iexact=username)
                | Q(profile__display_name__iexact=username)
            )
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            # Run the hasher anyway to keep timing consistent
            User().set_password(password)
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
