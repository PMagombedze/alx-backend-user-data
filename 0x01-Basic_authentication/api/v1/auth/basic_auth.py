#!/usr/bin/env python3
"""
Defines a BasicAuth class
"""
import base64
from typing import Tuple, TypeVar, Union, Optional

from api.v1.auth.auth import Auth
from api.v1.views.users import User


class BasicAuth(Auth):
    """
    Basic Authentication class implementation
    """
    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> Optional[str]:
        """authorization"""
        if isinstance(authorization_header, str) and authorization_header.startswith('Basic '):
            return authorization_header[6:]
        return None

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> Optional[str]:
        """
        Base64 encode authorization_header
        """
        if isinstance(base64_authorization_header, str):
            try:
                return base64.b64decode(base64_authorization_header).decode('utf-8')
            except Exception:
                pass
        return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract creds
        """
        if isinstance(decoded_base64_authorization_header, str) and ":" in decoded_base64_authorization_header:
            user_email, *user_pwd = decoded_base64_authorization_header.split(':')
            return user_email, ':'.join(user_pwd)
        return None, None

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> Union[TypeVar('User'), None]:
        """
        Gets the User instance based on given email and password
        """
        if isinstance(user_email, str) and isinstance(user_pwd, str):
            User.load_from_file()
            if User.count() > 0:
                users = User.search({'email': user_email})
                for user in users:
                    if user.is_valid_password(user_pwd):
                        return user
        return None

    def current_user(self, request=None) -> Optional[TypeVar('User')]:
        """
        Loads the current_user object
        """
        email, password = self.extract_user_credentials(
            self.decode_base64_authorization_header(
                self.extract_base64_authorization_header(
                    self.authorization_header(request=request)))
        )
        print(email, password)
        return self.user_object_from_credentials(email, password)
