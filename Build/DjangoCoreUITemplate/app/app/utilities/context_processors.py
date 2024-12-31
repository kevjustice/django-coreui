# context_processors.py
from django.conf import settings

def settings_context(request):
    """Make settings available in all templates"""
    return {
        'settings': settings
    }