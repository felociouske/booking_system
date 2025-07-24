from pathlib import Path
import os
from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='unsafe-default-secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

#DEBUG = True

#ALLOWED_HOSTS = [host.strip() for host in config('ALLOWED_HOSTS', default='localhost,127.0.0.1',).split(',')]
#ALLOWED_HOSTS = ['192.168.0.102','127.0.0.1']  # For development purposes only, use specific hosts in production
ALLOWED_HOSTS = ['web-production-0418c.up.railway.app', '127.0.0.1', 'localhost']

CSRF_TRUSTED_ORIGINS = [
    os.getenv("CSRF_ORIGIN", "https://web-production-0418c.up.railway.app")
]


# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'bookings',
    'payment',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'room_booking.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'room_booking.wsgi.application'

#Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'lwdQEIyBKbbVFSfOSgQkjEOuGVpFSCYD',
        'HOST': 'postgres.railway.internal',
        'PORT': '5432',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_L10N = True
USE_TZ = True
USE_I18N = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Login
LOGIN_REDIRECT_URL = '/accounts/student/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# USE_X_FORWARDED_HOST = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

JAZZMIN_SETTINGS = {
    "site_title": "JKUAT Admin",
    "site_header": "JKUAT Dashboard",
    "site_brand": "JKUSOS Club",
    "site_logo": "images/jkuat_logo.png",  # Place this in static/images/
    "login_logo": "images/jkuat_logo.png",
    "login_logo_dark": "images/jkuat_logo.png",
    "welcome_sign": "Welcome to JKUAT Admin Panel",
    "copyright": "JKUAT © 2025",
    "search_model": ["accounts.Member", "events.Event"],

    "topmenu_links": [
        {"name": "Home", "url": "/", "permissions": ["auth.view_user"]},
        {"model": "auth.User"},
        {"app": "accounts"},
    ],

    "usermenu_links": [
        {"name": "Profile", "url": "/admin/auth/user/", "icon": "fas fa-user"},
        {"name": "Logout", "url": "admin:logout", "icon": "fas fa-sign-out-alt"},
    ],

    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["accounts", "bookings", "payments"],

    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "accounts.Member": "fas fa-id-card",
        "events.Event": "fas fa-calendar-alt",
    },

    "custom_css": "css/custom_admin.css",  # Your custom overrides (see below)
    "custom_js": None,
    "show_ui_builder": False,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",  # base theme (bootstrap)
    "dark_mode_theme": "darkly",  # optional dark mode

    # Primary colors
    "primary": "gold",
    "accent": "amber",

    # Styling
    "body_small_text": False,
    "navbar_small_text": False,
    "footer_small_text": False,
    "sidebar_small_text": False,
    "brand_small_text": False,

    "sidebar_nav_flat_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_child_hide": False,

    "sidebar_color": "dark",
    "navbar_color": "black",
    "accent": "warning",

    "button_classes": {
        "primary": "btn btn-warning rounded-pill",
        "secondary": "btn btn-secondary rounded-pill",
        "info": "btn btn-info rounded-pill",
        "success": "btn btn-success rounded-pill",
        "danger": "btn btn-danger rounded-pill",
        "warning": "btn btn-warning rounded-pill",
    },

    "actions_sticky_top": True,
}
