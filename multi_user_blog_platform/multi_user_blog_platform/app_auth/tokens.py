from django.contrib.auth import tokens
import six


class ActivateAccountResetPasswordTokenGenerator(tokens.PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
    

account_activate_password_reset_token_generator = ActivateAccountResetPasswordTokenGenerator()