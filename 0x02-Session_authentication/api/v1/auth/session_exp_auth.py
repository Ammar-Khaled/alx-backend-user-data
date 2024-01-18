#!/usr/bin/env python3
"""Session Auth Module."""


from datetime import datetime, timedelta
from os import getenv
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class."""
    def __init__(self):
        """init method."""
        self.session_duration = int(getenv('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        """Create a Session ID."""
        try:
            session_id = super().create_session(user_id)
        except Exception:
            return None

        session_dictionary = {'user_id': user_id, 'created_at': datetime.now()}

        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return user ID based on `session_id`."""
        if not session_id:
            return None

        if type(session_id) != str:
            return None

        if session_id not in self.user_id_by_session_id.keys():
            return None

        session_dict = self.user_id_by_session_id.get(session_id)

        if not session_dict or 'created_at' not in session_dict.keys():
            return None

        user_id = session_dict.get('user_id')
        if self.session_duration <= 0:
            return user_id

        created_at = session_dict.get('created_at')
        session_duration = timedelta(seconds=self.session_duration)
        if created_at + session_duration < datetime.now():
            return None

        return user_id
