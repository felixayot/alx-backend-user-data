#!/usr/bin/env python3
"""Module for authenticated session expiration."""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class."""

    def __init__(self):
        """Initialize the class."""
        SESSION_DURATION = getenv('SESSION_DURATION')
        if SESSION_DURATION is None:
            self.session_duration = 0
        else:
            self.session_duration = int(SESSION_DURATION)

    def create_session(self, user_id=None):
        """Create a session."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return a User ID based on a Session ID."""
        if session_id is None:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        created_at = session_dict.get('created_at')
        if created_at is None:
            return None
        if (datetime.now() - created_at) > \
                timedelta(seconds=self.session_duration):
            return None
        return session_dict.get('user_id')
