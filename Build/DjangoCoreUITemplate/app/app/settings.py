"""
Django-CoreUI settings file

// Copyright (c) 2025 Matice/Kevin Justice
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

"""
from pathlib import Path
import os
from app.utilities import is_pg_available
from django.utils.safestring import mark_safe
import logging
from app.utilities.is_pg_available import postgres_connection

# you should remove this section when in docker production
from dotenv import load_dotenv
# Load .env file
load_dotenv()
#SSL related


# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent
APPEND_SLASH = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-4)56uhk#wf+cm65c!(y*a#w=a3h#-j%s@!htw67^76krw9=w5c')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
DJDTToolbar = True 
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')

# SECURITY SETTINGS
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Sessions will clear when browser closes
DISABLE_REGISTRATION = os.environ.get('DISABLE_REGISTRATION', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1").split(",")
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_PROXY_SSL_HEADER = None

# APPLICATION SETTINGS
VERSION = '1.0.0'
APP_SETTING_ID = VERSION  # Change this to force reinitialization of default_app_settings

DEFAULT_APP_SETTINGS = {
    'appname': 'My App',
    'full_logo_url': '/static/assets/brand/coreui.svg#full',
    'signet_logo_url': '/static/assets/brand/coreui.svg#signet',
    'favicon': '/static/assets/favicon/favicon.ico',
    'meta_description': 'Description of My App',
    'appinfo': 'The greatest app',
    'copywright': '&nbsp;&copy; 2024 Kevin Justice',
    'poweredby': 'Powered by&nbsp;<a href="https://matice.com">Matice</a>',
    'head_stylesheets': mark_safe("""
        <link rel="stylesheet" href="/static/css/mystyles.css">
        <style>
            body {background-color-BADCSS:#fff;}
        </style>                   
    """),
    'site_javascripts': mark_safe("""
        <script src="/static/js/myjs.js"></script>
        <script>
            alert('You really should look at the settings.py file and update the defaults!');
        </script>
    """),
    'header_disabled': False,
    'menu_breadcrumbs_disabled': False,
    'menu_header_leftmenu_disabled': False,
    'menu_user_interactions_disabled': False,
    'menu_user_contrast_disabled': False,
    'menu_user_avatar_menu_disabled': False,
    'top_menu_disabled': False,
    'footer_disabled': False,
    'menu_sidebar_disabled': False,
    'active_theme': 'dark',\
    'max_breadcrumbs': 5,
}

# Application definition
INSTALLED_APPS = [
    'app',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'app.middleware.middleware.SessionToContextMiddleware',
    'app.middleware.middleware.BreadcrumbMiddleware',
    'app.middleware.middleware.MenuMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app.middleware.initial_setup.InitialSetupMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'app.middleware.middleware.CacheControlMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app.middleware.context_processors.settings_context',
            ],                
            'libraries':{
                'menu_tags': 'app.templatetags.menu_tags',
            }
        },
    },
]

# Configure whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True
WHITENOISE_MAX_AGE = 31536000  # 1 year in seconds
WHITENOISE_COMPRESSION_ENABLED = True

WSGI_APPLICATION = 'app.wsgi.application'

# DATABASE CONFIGURATION
DATABASE_TYPE = os.environ.get("DATABASE_TYPE", "sqlite").lower()
logger = logging.getLogger('django')

# Define SQLite configuration once to avoid repetition
SQLITE_CONFIG = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Define PostgreSQL configuration
POSTGRESQL_CONFIG = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PORT": os.environ.get("POSTGRES_PORT"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "NAME": os.environ.get("POSTGRES_DATABASE"),
        "CONN_MAX_AGE": 60,  # 1 minute connection persistence
        "OPTIONS": {
            "connect_timeout": 10,
        },
    }
}

if DATABASE_TYPE == "postgres":
    if postgres_connection():
        logger.info("Successfully connected to PostgreSQL. Using PostgreSQL as database backend.")
        DATABASES = POSTGRESQL_CONFIG
    else:
        logger.warning(
            "Failed to connect to PostgreSQL. Falling back to SQLite. "
            "Check your PostgreSQL connection settings in the environment variables."
        )
        DATABASES = SQLITE_CONFIG
else:
    logger.info("Using SQLite as database backend.")
    DATABASES = SQLITE_CONFIG

# CACHE CONFIGURATION
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': '',
    }
}

# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {
            'user_attributes': ('username', 'email', 'first_name', 'last_name'),
            'max_similarity': 0.7,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# INTERNATIONALIZATION
LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE', 'en-us')
TIME_ZONE = os.environ.get('TIMEZONE', 'UTC')
USE_I18N = True
USE_TZ = True

# STATIC FILES
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
STATIC_FILES_HEADERS = {
    'Cache-Control': 'max-age=86400',  # Cache for 24 hours
}

# MEDIA FILES
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# FILE UPLOAD SETTINGS
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440  # 2.5 MB
FILE_UPLOAD_PERMISSIONS = 0o644

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# EMAIL CONFIGURATION
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'webmaster@localhost')

# SESSION CONFIGURATION
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# AUTHENTICATION SETTINGS
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
REGISTER_URL = '/register'



# LOGGING CONFIGURATION
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'level': 'DEBUG',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.server': {  # This specifically targets the development server logs
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django': {
            'handlers': ['console', 'file'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'app': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'app.utilities.menu_manager': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Ensure the logs directory exists
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Development-specific settings
if DJDTToolbar:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
    INTERNAL_IPS = ['127.0.0.1']

    # Disable certain security settings in development
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
