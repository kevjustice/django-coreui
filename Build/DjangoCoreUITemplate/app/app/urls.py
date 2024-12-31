"""
URL Configuration for the application
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.core.management import call_command
from app import views

# Run initial setup check
#try:
#    if not User.objects.filter(is_superuser=True).exists():
#        call_command('initial_setup')
#except:
#    pass  # Database might not be ready yet

urlpatterns = [
    # Main URLs
    path('', views.HomeView.as_view(), name='home'),

    # Example URLS
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('icons/', views.IconsView.as_view(), name='icons'),
    
    # Django Admin
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('login/', views.CustomLoginView.as_view(),name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user/logout/', views.logout_view, name='user_logout'),  # Alias for backward compatibility
    
    # User Management URLs
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/add/', views.UserCreateView.as_view(), name='user_add'),
    path('users/<int:pk>/change/', views.UserUpdateView.as_view(), name='user_change'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('users/<int:pk>/password/', views.SetPasswordView.as_view(), name='set_password'),
    path('users/change_password/', views.PasswordChangeView.as_view(), name='change_password'),
    path('initial-setup/', views.InitialSetupView.as_view(), name='initial_setup'),
    path('register/', views.UserRegister.as_view(), name='register'),
    
    # Email Testing URLs 
    path('admin-test-email/', views.test_email_view, name='test_email'),
    path('admin-comprehensive-email-test/', views.comprehensive_email_test_view, name='comprehensive_email_test'),
    path('admin/ajax-test-email/', views.ajax_test_email, name='ajax_test_email'),
    
    # Password Reset URLs
    path('password_reset/',auth_views.PasswordResetView.as_view(    template_name='admin/password_reset.html'),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(    template_name='admin/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(    template_name='admin/password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(    template_name='admin/password_reset_complete.html'),name='password_reset_complete'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler404 = 'app.views.custom_404_view'

# Optional: Add debug toolbar URLs if DEBUG is True
if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass

# Optional: Add media files serving in development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT
    )
