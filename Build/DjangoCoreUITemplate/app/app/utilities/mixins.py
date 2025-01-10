# mixins.py

from .session_manager import UserSessionManager
from .menu_manager import MenuManager
from django.conf import settings


class BaseContextMixin:
    """Mixin to provide base context for all views"""
    def get_base_context(self, request):
        session = UserSessionManager(request)
        menu_manager = MenuManager.ensure_default_menus(session)
        all_settings = session.get_all_settings()

        return {
            'sidebar': menu_manager.get_menu('sidebar', request.user.is_authenticated),
            'header_left_menu': menu_manager.get_menu('header_left_menu', request.user.is_authenticated),
            'header_right_menu': menu_manager.get_menu('header_right_menu', request.user.is_authenticated),
            'user_menu': menu_manager.get_menu('user_menu', request.user.is_authenticated),
            'menu_user_interactions_disabled': settings.DEFAULT_APP_SETTINGS['menu_user_interactions_disabled'],
            'menu_user_contrast_disabled': settings.DEFAULT_APP_SETTINGS['menu_user_contrast_disabled'],
            'menu_user_avatar_menu_disabled': settings.DEFAULT_APP_SETTINGS['menu_user_avatar_menu_disabled'],
            'settings': all_settings,
            'title': settings.DEFAULT_APP_SETTINGS['appname'] + ": ",
        }
