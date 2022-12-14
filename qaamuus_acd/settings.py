"""
Django settings for qaamuus_acd project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from urllib.parse import urlparse
from decouple import config
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR=os.path.join(BASE_DIR,'templates')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

SECRET_KEY=config('SECRET_KEY')

DEBUG = eval(config('DEBUG'))
ALLOWED_HOSTS=config("ALLOWED_HOSTS").split(',')

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'corsheaders',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'api',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'ckeditor',
    'a_webinar',
    'a_system',
    'rest_framework',
]


    # 'rest_framework',
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.common.CommonMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
JAZZMIN_SETTINGS = {
     "site_title": "QAAMUUS-ACADEMY",
     "site_header": "E-Learning",
    #  "site_logo": "/images/logo/logo-4.png",
     "copyright": "copyright @qaamuus academy 2021",
     "search_model": "auth.User",
     "user_avatar": None,
     "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "api.QaCourses": "fas fa-chalkboard-teacher",
        "api.Lessons": "fas fa-book-reader",
        "api.UserProfile": "fas fa-users",
    },
}
# JAZZMIN_UI_TWEAKS = {
#     "theme": "flatly",
#     "dark_mode_theme": "darkly",
# }

ROOT_URLCONF = 'qaamuus_acd.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'a_system.views.userProfileInfo', 
            ],
        },
    },
]

WSGI_APPLICATION = 'qaamuus_acd.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    )
}





SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),

    'AUTH_HEADER_TYPES': ('Bearer',),

}






# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config("NAME"),
        'USER': config("USER"),
        'PASSWORD': config("PASSWORD"),
        'HOST': config("HOST"),
        'PORT': config("PORT"),
    }
}

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dw6vcihvc',
    'API_KEY': '563644916747992',
    'API_SECRET': 'LT3kD9H-tJO_gQLL8PIeSoPSgDI'
}

# https://qaamuusstaticfiles.sgp1.digitaloceanspaces.com

# top DO00QBBDKQZHJH7DX3G6
# bottom zyb8shFkk/69XwBOKOhjqEor9yw/NwOeEF/aJlKK+wo

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Mogadishu'
# TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT=os.path.join(BASE_DIR,'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
MEDIA_URL='/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

MEDIA_ROOT=os.path.join(BASE_DIR,'media')

# from .cdn.conf import *
CSRF_TRUSTED_ORIGINS =["https://qaamuusbackend.up.railway.app","http://localhost:3000/","http://localhost","http://127.0.0.1:3000/"]
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = [
# 'http://localhost:3000',
# 'http://127.0.0.1:3000'
# ]
CORS_ALLOW_CREDENTIALS = True
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

# STATIC_ROOT = os.path.join(BASE_DIR, "static")
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SMTP 
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = int(config('EMAIL_PORT'))
EMAIL_USE_TLS = eval(config('EMAIL_USE_TLS'))
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
