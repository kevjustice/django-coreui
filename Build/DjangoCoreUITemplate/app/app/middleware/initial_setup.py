# app/middleware/initial_setup.py
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User

class InitialSetupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip check for static files and the setup page itself
        if request.path.startswith('/static/') or request.path == '/initial-setup/':
            return self.get_response(request)

        # Check if any superuser exists
        if not User.objects.filter(is_superuser=True).exists():
            return redirect('initial_setup')

        return self.get_response(request)
