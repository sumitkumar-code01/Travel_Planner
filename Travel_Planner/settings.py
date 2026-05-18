"""
Django settings for Travel_Planner project.
Systematic and Fixed Version for: Introduction -> Login -> Dashboard
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f3p5y@s%rq7z$m9rk%s3nwvbx*vx_to)jx86mn@l^5$@qy+v4u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# --- Application definition ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'trips',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Travel_Planner.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'trips' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Travel_Planner.wsgi.application'

# --- Database ---

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- Password validation ---

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internationalization ---

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- Static files (CSS, JavaScript, Images) ---

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static", 
]

# --- Media files (Uploads) ---

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- Login / Logout Logic (FIXED & SYSTEMATIC) ---


LOGIN_URL = '/login/'

# 2. Login button click karne ke baad user kahan jayega
LOGIN_REDIRECT_URL = '/add_trip/'

# 3. Logout karne ke baad user kahan jayega (Intro Page)
LOGOUT_REDIRECT_URL = '/'

# 4. GET request se logout allow karne ke liye (Important for manual logout)
LOGOUT_ON_GET = True

LOGIN_REDIRECT_URL = 'login_check'

LOGOUT_REDIRECT_URL = 'landing'


# Django settings.py
CSRF_COOKIE_SECURE = False  # Localhost par runs karne ke liye False rakhein
CSRF_COOKIE_HTTPONLY = True
# Agar aap localhost standard terminal use kar rahe hain toh iski zaroorat nahi, 
# lekin back-button issue ke liye ye help karta hai:
CSRF_USE_SESSIONS = True