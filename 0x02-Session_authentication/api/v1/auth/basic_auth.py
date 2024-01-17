#!/usr/bin/env python3
"""Basic Auth Module."""


from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """BasicAuth class."""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Return the Base64 part of the Authorization header."""
        if not authorization_header:
            return None

        if type(authorization_header) != str:
            return None

        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header.split()[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """Return the decoded value of a Base64 string."""
        if not base64_authorization_header:
            return None

        if type(base64_authorization_header) != str:
            return None

        try:
            import base64
            decoded_b64 = base64.b64decode(base64_authorization_header)
            return decoded_b64.decode()
        except Exception:
            return None

    def extract_user_credentials(
                                self,
                                decoded_base64_authorization_header: str
                                ) -> (str, str):
        """Return the user email and password from the Base64 decoded value."""
        if not decoded_base64_authorization_header:
            return (None, None)

        if type(decoded_base64_authorization_header) != str:
            return (None, None)

        if decoded_base64_authorization_header.find(':') == -1:
            return (None, None)

        credentials = decoded_base64_authorization_header.split(':', 1)
        return (credentials[0], credentials[1])

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Return the `User` instance based on his email and password."""
        if not user_email or type(user_email) != str:
            return None

        if not user_pwd or type(user_pwd) != str:
            return None

        try:
            search_users = User.search({'email': user_email})
        except Exception:
            return None

        for user in search_users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Return the `User` instance of the `request`."""
        if not request:
            return None

        auth_header = self.authorization_header(request)
        if not auth_header:
            return None

        base64_header = self.extract_base64_authorization_header(auth_header)
        if not base64_header:
            return None

        d64_header = self.decode_base64_authorization_header(base64_header)
        if not d64_header:
            return None

        creds = self.extract_user_credentials(d64_header)
        if creds == (None, None):
            return None

        return self.user_object_from_credentials(creds[0], creds[1])
