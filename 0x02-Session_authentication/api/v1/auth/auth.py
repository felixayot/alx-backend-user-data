#!/usr/bin/env python3
""" Module of User Authentication
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require auth
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        if any([p.endswith('*') and path.startswith(p[:-1])
               for p in excluded_paths]):
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user
        """
        return None

    def session_cookie(self, request=None):
        """Session cookie
        """
        if request is None:
            return None
        SESSION_NAME = getenv('SESSION_NAME')
        if SESSION_NAME is None:
            return None
        return request.cookies.get(SESSION_NAME)
