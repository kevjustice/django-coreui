# session_manager.py
import logging
import re
from datetime import datetime
from typing import Any, Dict, Optional
from urllib.parse import urlparse

from django.conf import settings
from django.contrib import messages
from django.contrib.messages import get_messages
from django.urls import resolve

logger = logging.getLogger(__name__)


class UserSessionManager:
    """Manage user session data"""

    def __init__(self, request):
        self.session = getattr(request, "session", None)
        self.modified = False

        # If no session is available, use a dummy session
        if self.session is None:
            logger.debug("No session available, using default settings")
            self._use_default_settings()
            return

        # Check settings version and reset if needed
        current_settings = self.session.get("app_settings", {})
        if current_settings.get("settings_version") != settings.APP_SETTING_ID:
            logger.debug("Settings version mismatch, reinitializing")
            self.initialize_settings()
            return

        # Initialize settings if they haven't been set yet
        if "app_settings" not in self.session:
            logger.debug("Initializing settings in session")
            self.initialize_settings()

    def __delitem__(self, key: str) -> None:
        """Delete item using dictionary syntax"""
        if self.is_using_defaults():
            if key in self._settings:
                del self._settings[key]
            return

        if "app_settings" in self.session:
            app_settings = self.session["app_settings"]
            if key in app_settings:
                del app_settings[key]
                self.session["app_settings"] = app_settings
                self.modified = True

    def __getattr__(self, name):
        """Handle attribute access when no session is available"""
        if not hasattr(self, "session"):
            self._use_default_settings()
        return super().__getattribute__(name)

    def __getitem__(self, key):
        return self.session[key]

    def __setitem__(self, key, value):
        self.session[key] = value
        self.session.modified = True  # Make sure this is set>

    def _use_default_settings(self):
        """Use default settings when no session is available"""
        self._dummy_session = True
        self._settings = settings.DEFAULT_APP_SETTINGS.copy()
        self._dummy_data = {
            "app_settings": self._settings,
            "breadcrumbs": [],
        }

    def _format_url_to_name(self, url):
        """Convert URL's last segment to camel case name with additional handling"""
        path = urlparse(url).path
        last_segment = path.rstrip("/").split("/")[-1]
        name = re.sub(r"\.[^.]+$", "", last_segment)
        name = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", name)
        words = re.split(r"[^a-zA-Z0-9]+", name)
        words = [word.strip() for word in words if word.strip()]
        name = " ".join(word.capitalize() for word in words)

        abbreviations = {"Url": "URL", "Id": "ID", "Html": "HTML"}
        for original, replacement in abbreviations.items():
            name = name.replace(original, replacement)

        return name

    def _validate_breadcrumb(self, breadcrumb):
        """Validate breadcrumb data structure"""
        if not isinstance(breadcrumb, dict):
            return False
        required_keys = ["url", "title"]
        return all(key in breadcrumb for key in required_keys)

    def _validate_key_value(self, key: str, value: Any) -> bool:
        """Validate key and value before storing"""
        if not isinstance(key, str):
            logger.warning(f"Invalid key type: {type(key)}")
            return False
        return True

    def _get_session_settings(self) -> Dict[str, Any]:
        """Safely get settings from session"""
        try:
            if self.is_using_defaults():
                return self._settings
            return self.session.get("app_settings", {})
        except Exception as e:
            logger.warning(f"Error accessing session settings: {e}")
            return settings.DEFAULT_APP_SETTINGS.copy()

    def add_breadcrumb(self, path):
        """Add a path to breadcrumbs, handling duplicates by moving them to the end"""
        if self.is_using_defaults():
            return

        # Get current breadcrumbs (now a list of dictionaries with title and path)
        breadcrumbs = self.session.get("breadcrumbs", [])
        max_crumbs = self.get_setting("max_breadcrumbs", 5)
        pagetitle = self.get_page_title(path)
        
        # Create breadcrumb entry with both title and path
        new_crumb = {'title': pagetitle, 'url': path}

        # Remove existing entry with same title
        breadcrumbs = [b for b in breadcrumbs if b['title'] != pagetitle]

        # Add new breadcrumb
        breadcrumbs.append(new_crumb)

        # Trim to max length if needed
        if len(breadcrumbs) > max_crumbs:
            breadcrumbs = breadcrumbs[-max_crumbs:]

        # Update session
        self.session["breadcrumbs"] = breadcrumbs
        self.modified = True
        self.save()

    def clear_all(self) -> None:
        self.clear(self)

    def clear(self) -> None:
        # Clear messages
        storage = get_messages(self.request)
        for message in storage:
            pass  # Iterate through to clear them

        """Clear all session settings and reinitialize with defaults"""
        if self.is_using_defaults():
            self._settings = settings.DEFAULT_APP_SETTINGS.copy()
            return
        else:
            # Clear breadcrumbs
            if "breadcrumbs" in self.session:
                del self.session["breadcrumbs"]

            # Clear app settings
            if "app_settings" in self.session:
                del self.session["app_settings"]

        self.session["app_settings"] = settings.DEFAULT_APP_SETTINGS.copy()
        self.modified = True
        self.save()

    def clear_breadcrumbs(self):
        """Clear all breadcrumbs"""
        if self.is_using_defaults():
            return

        if "breadcrumbs" in self.session:
            del self.session["breadcrumbs"]
            self.modified = True
            self.save()

    def debug_info(self) -> Dict[str, Any]:
        """Get debug information about current state"""
        return {
            "using_defaults": self.is_using_defaults(),
            "has_session": hasattr(self, "session"),
            "is_modified": self.modified,
            "settings_count": len(self.get_all_settings()),
            "has_breadcrumbs": bool(self.get_breadcrumbs()),
        }

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from session settings"""
        if self.is_using_defaults():
            return self._settings.get(key, default)

        app_settings = self.session.get("app_settings", {})
        return app_settings.get(key, default)

    def _get_session_settings(self) -> Dict[str, Any]:
        """Safely get settings from session"""
        try:
            if self.is_using_defaults():
                return self._settings
            return self.session.get("app_settings", {})
        except Exception as e:
            logger.warning(f"Error accessing session settings: {e}")
            return settings.DEFAULT_APP_SETTINGS.copy()

    def get_all(self) -> Dict[str, Any]:
        """Get all settings"""
        if self.is_using_defaults():
            return self._settings

        if "app_settings" not in self.session:
            self.initialize_settings()
        return self.session.get("app_settings", settings.DEFAULT_APP_SETTINGS)
    
    def get_breadcrumbs(self):
        return self.session.get('breadcrumbs', [])
    
    # def get_breadcrumbs(self):
    #     """Get formatted breadcrumbs"""
    #     if self.is_using_defaults():
    #         return []

    #     crumbs = self.session.get("breadcrumbs", [])
    #     return [{"path": c["path"], "title": c["title"]} for c in crumbs]

    def get_page_title(self, url):
        """Get page title for URL"""
        try:
            resolver_match = resolve(url)
            # Try to get title from view
            if hasattr(resolver_match.func, "page_title"):
                return resolver_match.func.page_title

            # Default formatting based on URL name
            return resolver_match.url_name.replace("_", " ").title()
        except:
            return url.strip("/").split("/")[-1].replace("-", " ").title()

    def get_setting(self, key, default=None):
        """Get a setting value from session or default app settings"""
        if self.is_using_defaults():
            return settings.DEFAULT_APP_SETTINGS.get(key, default)

        app_settings = self.session.get("app_settings", {})
        return app_settings.get(key, default)

    def get_template_context(self) -> Dict[str, Any]:
        """Get context dictionary for templates"""
        return {
            "APP_SETTINGS": self.get_all_settings(),
            "DEFAULT_APP_SETTINGS": settings.DEFAULT_APP_SETTINGS,
            "is_using_defaults": self.is_using_defaults(),
            "active_theme": self.get_theme(),
        }

    def get_theme(self) -> str:
        """Get current theme setting"""
        return self.get("active_theme", "light")

    def has_key(self, key: str) -> bool:
        """Check if a key exists in session settings"""
        settings_dict = self._get_session_settings()
        return key in settings_dict

    def initialize_settings(self) -> None:
        """Initialize session with default settings from settings.py"""
        defaults = settings.DEFAULT_APP_SETTINGS.copy()
        defaults["settings_version"] = settings.APP_SETTING_ID  # Add version

        if self.is_using_defaults():
            self._settings = defaults
            return

        self.session["app_settings"] = defaults
        self.modified = True
        self.save()

    def is_home_page(self, url):
        """Check if URL is home page"""
        return url == "/" or url == ""

    def is_menu_feature_enabled(self, feature: str) -> bool:
        """Check if a menu feature is enabled"""
        return not self.get(f"menu_user_{feature}_disabled", False)

    def is_using_defaults(self) -> bool:
        """Check if using dummy session with default settings"""
        return hasattr(self, "_dummy_session")

    def items(self) -> list:
        """Get all setting items as (key, value) pairs"""
        settings_dict = self._get_session_settings()
        return list(settings_dict.items())

    def keys(self) -> list:
        """Get all setting keys"""
        settings_dict = self._get_session_settings()
        return list(settings_dict.keys())

    def pop(self, key: str, default: Any = None) -> Any:
        """Remove and return a value from session settings"""
        if self.is_using_defaults():
            return self._settings.pop(key, default)

        app_settings = self._get_session_settings()
        value = app_settings.pop(key, default)
        self.session["app_settings"] = app_settings
        self.modified = True
        self.save()
        return value

    def remove_last_breadcrumb(self):
        """Remove the last breadcrumb"""
        if self.is_using_defaults():
            return

        breadcrumbs = self.session.get("breadcrumbs", [])
        if breadcrumbs:
            breadcrumbs.pop()
            self.session["breadcrumbs"] = breadcrumbs
            self.modified = True
            self.save()

    def reset_to_defaults(self) -> None:
        """Reset settings to default values from settings.py"""
        self.initialize_settings()

    def save(self) -> None:
        """Save changes to session"""
        if self.is_using_defaults():
            return

        if self.modified:
            self.session.modified = True
            self.modified = False

    def set(self, key: str, value: Any) -> None:
        """Set a value in session settings"""
        if not self._validate_key_value(key, value):
            return

        if self.is_using_defaults():
            self._settings[key] = value
            return

        app_settings = self._get_session_settings()
        app_settings[key] = value
        self.session["app_settings"] = app_settings
        self.modified = True
        self.save()

    def set_menu_feature(self, feature: str, enabled: bool) -> None:
        """Enable or disable a menu feature"""
        self.set(f"menu_user_{feature}_disabled", not enabled)

    def set_theme(self, theme: str) -> None:
        """Set current theme"""
        self.set("active_theme", theme)

    def toggle_menu_feature(self, feature: str) -> bool:
        """Toggle a menu feature between enabled and disabled"""
        current_state = self.is_menu_feature_enabled(feature)
        self.set_menu_feature(feature, not current_state)
        return not current_state

    def toggle_theme(self) -> str:
        """Toggle between light and dark theme"""
        current_theme = self.get_theme()
        new_theme = "dark" if current_theme == "light" else "light"
        self.set_theme(new_theme)
        return new_theme

    def update(self, settings_dict: Dict[str, Any]) -> None:
        """Update multiple settings at once"""
        if not isinstance(settings_dict, dict):
            logger.warning(f"Invalid settings type: {type(settings_dict)}")
            return

        for key, value in settings_dict.items():
            self.set(key, value)

    def values(self) -> list:
        """Get all setting values"""
        settings_dict = self._get_session_settings()
        return list(settings_dict.values())
