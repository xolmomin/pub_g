from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import constant_time_compare
from django.utils.http import base36_to_int
from six import text_type

from myapp.models import PUser
from pub_g import settings


class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return text_type(user.is_active) + text_type(user.pk) + text_type(timestamp)

    def check_token(self, user, token):
        if not (user and token):
            return False
            # Parse the token
        try:
            ts_b36, _ = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

            # Check that the timestamp/uid has not been tampered with
        if not constant_time_compare(self._make_token_with_timestamp(user, ts), token):
            return False

            # Check the timestamp is within limit. Timestamps are rounded to
            # midnight (server time) providing a resolution of only 1 day. If a
            # link is generated 5 minutes before midnight and used 6 minutes later,
            # that counts as 1 day. Therefore, PASSWORD_RESET_TIMEOUT_DAYS = 1 means
            # "at least 1 day, could be up to 2."
        if (self._num_days(self._today()) - ts) > settings.PASSWORD_RESET_TIMEOUT_DAYS:
            User.objects.filter(id=user.id).delete()
            PUser.objects.filter(user=user).delete()
            return False

        return True


token_generator = AppTokenGenerator()
