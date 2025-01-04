# app/enums.py
from enum import Enum, auto

class AuthRequirement(Enum):
    """Authentication requirements"""
    AUTH_ONLY = "auth_only"      # Only show when authenticated
    UNAUTH_ONLY = "unauth_only"  # Only show when not authenticated
    ALL = "all"                  # Show for all users

class MenuPosition(Enum):
    """Menu item positions"""
    TOP = "top"
    BOTTOM = "bottom"
    BEFORE = "before"
    AFTER = "after"

class MenuItemType(Enum):
    """Menu item types"""
    HEADER = "header"
    LINK = "link"
    SEPARATOR = "separator"
    DROPDOWN = "dropdown"