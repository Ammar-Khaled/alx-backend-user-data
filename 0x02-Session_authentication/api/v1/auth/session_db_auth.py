#!/usr/bin/env python3
"""SessionDBAuth Module."""
from flask import request
from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class."""
    def create_session(self, user_id=None):
        """Create and store a new instance of UserSession and
        return the Session ID."""
        session_id = super().create_session(user_id)
        if session_id and type(session_id) == str:
            user_session = UserSession({
                'user_id': user_id,
                'session_id': session_id
            })
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns the User ID by requesting `UserSession` in the database
        based on `session_id`."""
        try:
            user_sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None

        if len(user_sessions) <= 0:
            return None

        created_at = user_sessions[0].created_at
        session_duration = timedelta(seconds=self.session_duration)
        if created_at + session_duration < datetime.now():
            return None

        return user_sessions[0].user_id

    def destroy_session(self, request=None):
        """Destroy the `UserSession` based on the Session ID
        from the `request` cookie."""
        session_id = self.session_cookie(request)
        if not session_id:
            return False

        try:
            user_sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False

        if len(user_sessions) <= 0:
            return False

        user_sessions[0].remove()
        return True
