from typing import Any, Dict, Optional
from django.conf import settings
from django.urls import resolve
from urllib.parse import urlparse
import re

class UserSessionManager:
    """Manage user session data"""
    
    def __init__(self, request):
        self.session = request.session
        self.modified = False
        
        # Initialize settings if they haven't been set yet
        if 'app_settings' not in self.session:
            self.initialize_settings()

    def __delitem__(self, key: str) -> None:
        """Delete item using dictionary syntax"""
        if 'app_settings' in self.session:
            app_settings = self.session['app_settings']
            if key in app_settings:
                del app_settings[key]
                self.session['app_settings'] = app_settings
                self.modified = True

    def __getitem__(self, key: str) -> Any:
        """Get item using dictionary syntax"""
        return self.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        """Set item using dictionary syntax"""
        self.set(key, value)

    def _format_url_to_name(self, url):
        """Convert URL's last segment to camel case name with additional handling"""
        path = urlparse(url).path
        last_segment = path.rstrip('/').split('/')[-1]
        name = re.sub(r'\.[^.]+$', '', last_segment)
        name = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', name)
        words = re.split(r'[^a-zA-Z0-9]+', name)
        words = [word.strip() for word in words if word.strip()]
        name = ' '.join(word.capitalize() for word in words)
        
        abbreviations = {'Url': 'URL', 'Id': 'ID', 'Html': 'HTML'}
        for original, replacement in abbreviations.items():
            name = name.replace(original, replacement)
            
        return name

    def _validate_breadcrumb(self, breadcrumb):
        """Validate breadcrumb data structure"""
        if not isinstance(breadcrumb, dict):
            return False
        required_keys = ['url', 'title']
        return all(key in breadcrumb for key in required_keys)

    def add_breadcrumb(self, url):
        """Add a breadcrumb to the session"""
        breadcrumbs = self.session.get('breadcrumbs', [])
        max_breadcrumbs = self.get('max_breadcrumbs', 5)
        
        title = self.get_page_title(url)
        
        new_crumb = {
            'url': url,
            'title': title
        }

        # Check if this URL is already in breadcrumbs
        existing_urls = [crumb['url'] for crumb in breadcrumbs]
        if url in existing_urls:
            # Remove all crumbs after this one
            index = existing_urls.index(url)
            breadcrumbs = breadcrumbs[:index]
        
        # Add new crumb
        breadcrumbs.append(new_crumb)
        
        # Keep only last N breadcrumbs
        if len(breadcrumbs) > max_breadcrumbs:
            breadcrumbs = breadcrumbs[-max_breadcrumbs:]
        
        self.session['breadcrumbs'] = breadcrumbs
        self.modified = True
        self.save()

    def clear(self) -> None:
        """Clear all session settings and reinitialize with defaults"""
        self.session['app_settings'] = settings.DEFAULT_APP_SETTINGS.copy()
        self.modified = True
        self.save()

    def clear_breadcrumbs(self):
        """Clear all breadcrumbs"""
        if 'breadcrumbs' in self.session:
            del self.session['breadcrumbs']
            self.modified = True
            self.save()

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from session settings"""
        if 'app_settings' not in self.session:
            self.initialize_settings()
        
        app_settings = self.session.get('app_settings', {})
        return app_settings.get(key, default)

    def get_all_settings(self) -> Dict[str, Any]:
        """Get all settings from session"""
        if 'app_settings' not in self.session:
            self.initialize_settings()
        return self.session.get('app_settings', settings.DEFAULT_APP_SETTINGS)

    def get_breadcrumbs(self):
        """Get current breadcrumbs"""
        return self.session.get('breadcrumbs', [])

    def get_page_title(self, url):
        """Get page title for URL"""
        try:
            resolver_match = resolve(url)
            # Try to get title from view
            if hasattr(resolver_match.func, 'page_title'):
                return resolver_match.func.page_title
            
            # Default formatting based on URL name
            return resolver_match.url_name.replace('_', ' ').title()
        except:            
            return url.strip('/').split('/')[-1].replace('-', ' ').title()

    def get_theme(self) -> str:
        """Get current theme setting"""
        return self.get('active_theme', 'light')

    def has_key(self, key: str) -> bool:
        """Check if a key exists in session settings"""
        if 'app_settings' not in self.session:
            self.initialize_settings()
        return key in self.session['app_settings']

    def initialize_settings(self) -> None:
        """Initialize session with default settings from settings.py"""
        self.session['app_settings'] = settings.DEFAULT_APP_SETTINGS.copy()
        self.modified = True
        self.save()

    def is_home_page(self, url):
        """Check if URL is home page"""
        return url == '/' or url == ''

    def is_menu_feature_enabled(self, feature: str) -> bool:
        """Check if a menu feature is enabled"""
        return not self.get(f'menu_user_{feature}_disabled', False)

    def items(self) -> list:
        """Get all setting items as (key, value) pairs"""
        if 'app_settings' not in self.session:
            self.initialize_settings()
        return list(self.session['app_settings'].items())

    def keys(self) -> list:
        """Get all setting keys"""
        if 'app_settings' not in self.session:
            self.initialize_settings()
        return list(self.session['app_settings'].keys())

    def pop(self, key: str, default: Any = None) -> Any:
        """Remove and return a value from session settings"""
        if 'app_settings' not in self.session:
            self.initialize_settings()
        
        app_settings = self.session['app_settings']
        value = app_settings.pop(key, default)
        self.session['app_settings'] = app_settings
        self.modified = True
        self.save()
        return value

    def remove_last_breadcrumb(self):
        """Remove the last breadcrumb"""
        breadcrumbs = self.session.get('breadcrumbs', [])
        if breadcrumbs:
            breadcrumbs.pop()
            self.session['breadcrumbs'] = breadcrumbs
            self.modified = True
            self.save()

    def reset_to_defaults(self) -> None:
        """Reset settings to default values from settings.py"""
        self.initialize_settings()

    def save(self) -> None:
        """Save changes to session"""
        if self.modified:
            self.session.modified = True
            self.modified = False

    def set(self, key: str, value: Any) -> None:
        """Set a value in session settings"""
        if 'app_settings' not in self.session:
            self.initialize_settings()
        
        app_settings = self.session['app_settings']
        app_settings[key] = value
        self.session['app_settings'] = app_settings
        self.modified = True
        self.save()

    def set_menu_feature(self, feature: str, enabled: bool) -> None:
        """Enable or disable a menu feature"""
        self.set(f'menu_user_{feature}_disabled', not enabled)

    def set_theme(self, theme: str) -> None:
        """Set current theme"""
        self.set('active_theme', theme)

    def toggle_menu_feature(self, feature: str) -> bool:
        """Toggle a menu feature between enabled and disabled"""
        current_state = self.is_menu_feature_enabled(feature)
        self.set_menu_feature(feature, not current_state)
        return not current_state

    def toggle_theme(self) -> str:
        """Toggle between light and dark theme"""
        current_theme = self.get_theme()
        new_theme = 'dark' if current_theme == 'light' else 'light'
        self.set_theme(new_theme)
        return new_theme

    def update(self, settings_dict: Dict[str, Any]) -> None:
        """Update multiple settings at once"""
        if 'app_settings' not in self.session:
            self.initialize_settings()
        
        app_settings = self.session['app_settings']
        app_settings.update(settings_dict)
        self.session['app_settings'] = app_settings
        self.modified = True
        self.save()

    def values(self) -> list:
        """Get all setting values"""
        if 'app_settings' not in self.session:
            self.initialize_settings()
        return list(self.session['app_settings'].values())
