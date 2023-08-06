from django.contrib.auth.backends import ModelBackend
from oscar.apps.customer.auth_backends import EmailBackend
from django.contrib.auth import get_user_model
UserModel = get_user_model()


class EmailModelBackend(EmailBackend):
    """
    authentication class to login with the email address.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            if '@' not in username:
                user = UserModel.objects.get(username=username)
            else:
                user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
