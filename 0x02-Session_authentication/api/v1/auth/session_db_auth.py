#!/usr/bin/env python3
"""Module for user session authentication in db storage."""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class."""

    def create_session(self, user_id=None):
        """Create a session."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        kwargs = {'user_id': user_id, 'session_id': session_id}
        user_session = UserSession(**kwargs)
        user_session.save()
        UserSession.save_to_file()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return a User ID based on a Session ID."""
        if session_id is None:
            return None
        UserSession.load_from_file()
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return None
        user_session = user_session[0]
        expired_time = user_session.created_at + \
            timedelta(seconds=self.session_duration)
        if expired_time < datetime.utcnow():
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """Delete the user session / logout."""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_session = UserSession.search({'session_id': session_id})
        if user_session is None:
            return False
        user_session.remove()
        UserSession.save_to_file()
        return True
