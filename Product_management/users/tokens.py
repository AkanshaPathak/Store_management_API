# tokens.py
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Custom token generator for account activation
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Create a hash value using the user's primary key, timestamp, and active status
        return str(user.pk) + str(timestamp) + str(user.is_active)

# Instantiate the token generator for account activation
account_activation_token = TokenGenerator()
