#!/usr/bin/env python3
"""Auth Module."""


from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class."""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks whether `path` requires authentication."""
        if not path:
            return True

        if not excluded_paths or len(excluded_paths) == 0:
            return True

        if not path.endswith('/'):
            path += '/'

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """authorization_header method."""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current_user method."""
        return None
