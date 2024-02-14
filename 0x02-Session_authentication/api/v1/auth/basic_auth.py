#!/usr/bin/env python3
""" Module of User Authentication
using the Basic Authentication method
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """BasicAuth class
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extract base64 authorization header
        """
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None
        if authorization_header[:6] != 'Basic ':
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decode base64 authorization header
        """
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            dh = base64.b64decode(base64_authorization_header)
            return dh.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Extract user credentials
        """
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """User object from credentials
        """
        if user_email is None or user_pwd is None or not isinstance(
                user_email, str) or not isinstance(user_pwd, str):
            return None
        try:
            user = User.search({'email': user_email})
        except Exception:
            return None
        for u in user:
            if u.is_valid_password(user_pwd):
                return u
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        b64_auth_header = self.extract_base64_authorization_header(auth_header)
        if b64_auth_header is None:
            return None
        decoded_auth_header = self.decode_base64_authorization_header(
            b64_auth_header)
        if decoded_auth_header is None:
            return None
        user_email, user_pwd = self.extract_user_credentials(
            decoded_auth_header)
        if user_email is None or user_pwd is None:
            return None
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
