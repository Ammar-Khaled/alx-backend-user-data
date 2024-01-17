#!/usr/bin/env python3
"""Session Auth Module."""


from api.v1.auth.auth import Auth
import uuid


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
