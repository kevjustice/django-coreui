"""
Django views for the application
"""
from functools import wraps
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth import logout, update_session_auth_hash, get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.core.validators import validate_email
from django.core.exceptions import ValidationError, PermissionDenied
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    TemplateView, 
    ListView, 
    CreateView, 
    UpdateView, 
    DeleteView,
    FormView
)
from django.conf import settings

from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    CustomSetPasswordForm,
    InitialSetupForm,
    CustomLoginForm,
)
from .utilities.session_manager import UserSessionManager
from .utilities.menu_manager import MenuManager
from .utilities.email_tests import send_test_email, run_comprehensive_email_test
from .utilities.mixins import BaseContextMixin

import logging
import datetime
import json
import os

User = get_user_model()
logger = logging.getLogger(__name__)

def registration_enabled(function):
    def wrap(request, *args, **kwargs):
        if settings.DISABLE_REGISTRATION:
            raise PermissionDenied("Registration is currently disabled.")
        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def with_base_context(view_func):
    """Decorator to add base context to function-based views"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        context = BaseContextMixin().get_base_context(request)
        response = view_func(request, *args, base_context=context, **kwargs)
        return response
    return wrapper

class IconsView(BaseContextMixin, TemplateView):
    """View for displaying icons"""
    template_name = 'home/ui-icons.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_context = self.get_base_context(self.request)
        base_context['title'] = f"{base_context['title']}Icons"
        context.update(base_context)
        return context

class HomeView(BaseContextMixin, TemplateView):
    """Home page view"""
    template_name = 'base.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_context = self.get_base_context(self.request)
        base_context.update({
            'content': 'homepage html default here!',
            'menu_user_interactions_enabled': False,
            'menu_user_avatar_menu_disabled': True,
            'title': f"{base_context['title']}Home"
        })
        context.update(base_context)
        return context

class DashboardView(LoginRequiredMixin, BaseContextMixin, TemplateView):
    """Dashboard view for authenticated users"""
    template_name = 'home/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_context = self.get_base_context(self.request)
        base_context['title'] = f"{base_context['title']}Dashboard"
        context.update(base_context)
        return context
    
class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('dashboard')  # Change 'home' to your dashboard URL name
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

    def get_success_url(self):
        return self.success_url

@method_decorator(registration_enabled, name='dispatch')    
class UserRegister(CreateView):
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        # Add any additional processing here
        return response

class UserListView(LoginRequiredMixin, BaseContextMixin, ListView):
    """View for listing all users"""
    model = User
    template_name = 'admin/user_list.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_context = self.get_base_context(self.request)
        base_context['title'] = f"{base_context['title']}List Users"
        context.update(base_context)
        return context

class UserCreateView(LoginRequiredMixin, BaseContextMixin, CreateView):
    """View for creating new users"""
    model = User
    form_class = CustomUserCreationForm
    template_name = 'admin/user_add.html'
    success_url = reverse_lazy('user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_context = self.get_base_context(self.request)
        base_context['title'] = f"{base_context['title']}Add User"
        context.update(base_context)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'User created successfully.')
        return response

class UserUpdateView(LoginRequiredMixin, BaseContextMixin, UpdateView):
    """View for updating existing users"""
    model = User
    form_class = CustomUserChangeForm
    template_name = 'admin/user_change.html'
    success_url = reverse_lazy('user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_context = self.get_base_context(self.request)
        base_context['title'] = f"{base_context['title']}Edit User"
        context.update(base_context)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'User updated successfully.')
        return response

class UserDeleteView(LoginRequiredMixin, BaseContextMixin, DeleteView):
    """View for deleting users"""
    model = User
    template_name = 'admin/user_delete.html'
    success_url = reverse_lazy('user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_context = self.get_base_context(self.request)
        base_context['title'] = f"{base_context['title']}Delete User"
        context.update(base_context)
        return context

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'User deleted successfully.')
        return response

class PasswordChangeView(LoginRequiredMixin, BaseContextMixin, UpdateView):
    """View for changing user password"""
    form_class = PasswordChangeForm
    template_name = 'admin/user_change_password.html'
    success_url = reverse_lazy('user_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_context = self.get_base_context(self.request)
        base_context['title'] = f"{base_context['title']}Change Password"
        context.update(base_context)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, self.request.user)
        messages.success(self.request, 'Password changed successfully.')
        return response

class SetPasswordView(LoginRequiredMixin, BaseContextMixin, UpdateView):
    """View for setting user password"""
    model = User
    form_class = CustomSetPasswordForm
    template_name = 'admin/user_set_password.html'
    success_url = reverse_lazy('user_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.get_object()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_context = self.get_base_context(self.request)
        base_context['title'] = f"{base_context['title']}Set Password"
        context.update(base_context)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Password set successfully.')
        return response

@login_required
@with_base_context
@require_http_methods(["GET", "POST"])
def test_email_view(request, base_context):
    """View for testing email sending"""
    context = base_context
    context['title'] = f"{context['title']}Email Test"
    context['test_results'] = None

    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            validate_email(email)
            result = send_test_email(email)
            
            context['test_results'] = {
                'success': result.success,
                'message': result.message,
                'timestamp': result.timestamp,
                'error_details': result.error_details
            }

            if result.success:
                messages.success(request, 'Test email sent successfully!')
            else:
                messages.error(request, f'Failed to send test email: {result.error_details}')

        except ValidationError:
            messages.error(request, 'Please enter a valid email address.')
        except Exception as e:
            logger.exception('Error in test_email_view')
            messages.error(request, f'An unexpected error occurred: {str(e)}')

    return render(request, 'admin/test_email.html', context)

@login_required
@with_base_context
@require_http_methods(["GET", "POST"])
def comprehensive_email_test_view(request, base_context):

    email_settings = {
        'EMAIL_BACKEND': getattr(settings, 'EMAIL_BACKEND', 'Not configured'),
        'EMAIL_HOST': getattr(settings, 'EMAIL_HOST', 'Not configured'),
        'EMAIL_PORT': getattr(settings, 'EMAIL_PORT', 'Not configured'),
        'EMAIL_HOST_USER': getattr(settings, 'EMAIL_HOST_USER', 'Not configured'),
        'EMAIL_HOST_PASSWORD': getattr(settings, 'EMAIL_HOST_PASSWORD', 'Not configured'),
        'EMAIL_USE_TLS': getattr(settings, 'EMAIL_USE_TLS', 'Not configured'),
        'DEFAULT_FROM_EMAIL': getattr(settings, 'DEFAULT_FROM_EMAIL', 'Not configured'),

    }
    

    """View for comprehensive email testing"""
    context = base_context
    context['title'] = f"{context['title']}Comprehensive Email Test"
    context['test_results'] = None

    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            validate_email(email)
            results = run_comprehensive_email_test(email)
            
            context['test_results'] = {
                'configuration': {
                    'success': results['config'].success,
                    'message': results['config'].message,
                    'error_details': results['config'].error_details,
                    'timestamp': results['config'].timestamp
                },
                'smtp': {
                    'success': results['smtp'].success,
                    'message': results['smtp'].message,
                    'error_details': results['smtp'].error_details,
                    'timestamp': results['smtp'].timestamp
                },
                'email': {
                    'success': results['send'].success,
                    'message': results['send'].message,
                    'error_details': results['send'].error_details,
                    'timestamp': results['send'].timestamp
                },
                'email_settings': email_settings,
            }

            if all(r.success for r in results.values()):
                messages.success(request, 'All email tests completed successfully!')
            else:
                messages.warning(request, 'Some email tests failed. Check the results below.')

        except ValidationError:
            messages.error(request, 'Please enter a valid email address.')
        except Exception as e:
            logger.exception('Error in comprehensive_email_test_view')
            messages.error(request, f'An unexpected error occurred: {str(e)}')

    return render(request, 'admin/comprehensive_email_test.html', context)

@login_required
@require_http_methods(["POST"])
def ajax_test_email(request):
    """Ajax view for email testing"""
    try:
        email = request.POST.get('email')
        test_type = request.POST.get('test_type', 'simple')
        
        validate_email(email)
        
        if test_type == 'comprehensive':
            results = run_comprehensive_email_test(email)
            response_data = {
                'success': all(r.success for r in results.values()),
                'results': {
                    key: {
                        'success': result.success,
                        'message': result.message,
                        'error_details': result.error_details,
                        'timestamp': result.timestamp.isoformat()
                    }
                    for key, result in results.items()
                }
            }
        else:
            result = send_test_email(email)
            response_data = {
                'success': result.success,
                'message': result.message,
                'error_details': result.error_details,
                'timestamp': result.timestamp.isoformat()
            }
        
        return JsonResponse(response_data)
        
    except ValidationError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid email address'
        }, status=400)
    except Exception as e:
        logger.exception('Error in ajax_test_email')
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

def logout_view(request):
    """View for logging out users"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

def custom_404_view(request, exception):
    """Custom 404 error view"""
    return render(request, '404.html', status=404)

class InitialSetupView(FormView):
    template_name = 'setup/initial_setup.html'
    form_class = InitialSetupForm
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        # Redirect if superuser already exists
        if User.objects.filter(is_superuser=True).exists():
            messages.warning(request, 'Setup has already been completed.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Create superuser
        User.objects.create_superuser(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password1']
        )

        # Create .env file if it doesn't exist
        env_path = os.path.join(settings.BASE_DIR, '.env')
        if not os.path.exists(env_path):
            with open(env_path, 'w') as f:
                f.write(f"DJANGO_SUPERUSER_EMAIL={form.cleaned_data['email']}\n")
                f.write(f"DJANGO_SUPERUSER_USERNAME={form.cleaned_data['username']}\n")

        messages.success(self.request, 'Admin user created successfully. Please log in.')
        return super().form_valid(form)