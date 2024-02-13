#!/usr/bin/env python3
"""
auth
"""
from flask import request
from typing import List, Optional


class Auth:
    """API authentication"""
    def require_auth(self, path: str, excluded: List[str]) -> bool:
        """Requires authentication"""
        if not path or not excluded:
            return True

        for url in excluded:
            if url.endswith('*') and url[:-1] in path:
                return False
            if path in url or path + '/' in url:
                return False

        return True

    def authorization_header(self, request=None) -> Optional[str]:
        """Authorization header"""
        if request:
            return request.headers.get('Authorization')
        return None

    def current_user(self, request=None) -> None:
        """Logged in user"""
        return None
