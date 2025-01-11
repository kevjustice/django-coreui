"""
Middleware utilities
"""
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from app.models import AppSetting
from app.utilities.session_manager import UserSessionManager
from app.utilities.menu_manager import MenuManager
from app.utilities.request_utils import is_ajax

class CacheControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if any(request.path.endswith(ext) for ext in ['.map', '.scss', '.css']):
            response['Cache-Control'] = 'public, max-age=31536000, immutable'
            response['Expires'] = 'Thu, 31 Dec 2099 23:59:59 GMT'
            response['Pragma'] = 'cache'
        return response

class MenuMiddleware(MiddlewareMixin):
    """Middleware to process menu-related functionality"""
    
    def is_ajax(self, request):
        """Check if the request is AJAX"""
        return request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def __call__(self, request):
        """Process the request"""
        session = UserSessionManager(request)
        request.session_manager = session

        # If it's an AJAX request, skip the menu processing
        if not is_ajax(request):
            # Your menu processing code here
            pass

        response = self.get_response(request)
        return response

class SettingsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Initialize settings if needed
        AppSetting.initialize_settings()
        
        # Load settings into session
        if not request.is_ajax():  # Skip for AJAX requests
            session = UserSessionManager(request)
            settings_dict = AppSetting.load_settings()
            session['app_settings'] = settings_dict

        response = self.get_response(request)
        return response

class BreadcrumbMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self.should_track_breadcrumb(request):
            path = request.get_full_path()
            
            # Special handling for examples paths
            if path.startswith('/examples/'):
                # Only track '/examples/' instead of the full path
                path = '/examples/'
            
            session = UserSessionManager(request)
            session.add_breadcrumb(path)

        response = self.get_response(request)
        return response

    def should_track_breadcrumb(self, request):
        """Determine if this request should be tracked in breadcrumbs"""
        # Skip non-GET requests
        if request.method != 'GET':
            return False

        # Skip excluded paths
        excluded_paths = [
            '/static/',
            '/media/',
            #'/admin/',
            '/favicon.ico',
            '/api/',
            '/ajax/',
        ]
        
        path = request.path
        if any(path.startswith(excluded) for excluded in excluded_paths):
            return False

        # Skip AJAX requests
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return False

        try:
            # Get the resolved URL pattern
            resolver_match = resolve(request.path)
            
            # Skip certain URL names (optional)
            excluded_url_names = ['login', 'logout', 'password_reset']
            if resolver_match.url_name in excluded_url_names:
                return False
                
        except:
            # If URL doesn't resolve, skip it
            return False

        return True
