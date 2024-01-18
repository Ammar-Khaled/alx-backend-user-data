#!/usr/bin/env python3
"""Session Auth Module."""


from api.v1.auth.auth import Auth
import uuid

from models.user import User


class SessionAuth(Auth):
    """SessionAuth class."""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a Session ID for `user_id`."""
        if not user_id:
            return None

        if type(user_id) != str:
            return None

        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID based on `session_id`."""
        if not session_id:
            return None

        if type(session_id) != str:
            return None

        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Return the `User` instance based on a cookie value."""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Delete the user session (logout)."""
        if not request:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        if session_id in self.user_id_by_session_id:
            self.user_id_by_session_id.pop(session_id)
        return True
