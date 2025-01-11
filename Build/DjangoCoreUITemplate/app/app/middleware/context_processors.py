# context_processors.py
from django.conf import settings
from app.utilities.session_manager import UserSessionManager
import logging

logger = logging.getLogger(__name__)

def settings_context(request):
    """Make settings available in templates"""
    try:
        session_manager = UserSessionManager(request)
        return {
            'APP_SETTINGS': session_manager.get_all(),  # Changed from get_all_settings
            'DEFAULT_APP_SETTINGS': settings.DEFAULT_APP_SETTINGS,
            'is_using_defaults': session_manager.is_using_defaults(),
            'active_theme': session_manager.get_theme(),
            #'settings': settings,
        }
    except Exception as e:
        logger.warning(f"Failed to initialize session manager: {e}")
        return {
            'APP_SETTINGS': settings.DEFAULT_APP_SETTINGS,
            'DEFAULT_APP_SETTINGS': settings.DEFAULT_APP_SETTINGS,
            'is_using_defaults': True,
            'active_theme': 'dark',
            #'settings': settings,
        }
    #try:
    #    session_manager = UserSessionManager(request)
    #    app_settings = session_manager.get_all_settings()
    #    return context 
    #except Exception as e:
    #    logger.warning(f"Failed to initialize session manager: {e}")
    #    app_settings = settings.DEFAULT_APP_SETTINGS

    #    return {
    #        'DEFAULT_APP_SETTINGS': settings.DEFAULT_APP_SETTINGS,
    #        'APP_SETTINGS': app_settings,
    #        'settings': settings,
    #        'session_manager': session_manager,  # Optional: if you need direct access to methods
    #    }    