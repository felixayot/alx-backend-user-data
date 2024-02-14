#!/usr/bin/env python3
"""Module for session authentication."""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """SessionAuth class."""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session."""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        if session_id is None:
            return None
        __class__.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID based on a Session ID."""
        if session_id is None or not isinstance(session_id, str):
            return None
        return __class__.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Return a User instance based on a cookie value."""
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Delete the user session / logout."""
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        del __class__.user_id_by_session_id[session_cookie]
        return True
