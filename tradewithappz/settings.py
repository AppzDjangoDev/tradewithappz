"""
Django settings for tradewithappz project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
# from dotenv import load_dotenv

# load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', default='your secret key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', default='True')

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
if not DEBUG:
    #for production
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True



ALLOWED_HOSTS = ['*']

from django.contrib.messages import constants as message_constants
MESSAGE_LEVEL = message_constants.DEBUG

# Application definition

INSTALLED_APPS = [
    'account',
    'trading_tool',
    'fyersapi',
    "channels",
    'django_cron',
    'scheduler',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',
]

CRON_CLASSES = [
    'fyersapi.cron.MyCronJob',
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

ROOT_URLCONF = 'tradewithappz.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'tradewithappz.wsgi.application'
ASGI_APPLICATION = 'tradewithappz.asgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# CELERY SETTINGS
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TIMEZONE = 'Asia/Kolkata'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'appztechblog_db',
#         'USER': 'appz',
#         'PASSWORD': 'root',
#         'HOST': '0.0.0.0',  # Docker service name
#         'PORT': '5432',  # PostgreSQL default port
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# MEDIAFILE
MEDIA_URL = '/media/'


MEDIA_DIRS = [ os.path.join(BASE_DIR, 'media') ]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# user model assign to account.user
AUTH_USER_MODEL = 'account.User'

# massages
from django.contrib.messages import constants as messages

DATE_INPUT_FORMATS = [
    '%Y-%m-%d',  # Default format
]

# DEVELOPMENT_MODE=False  
DEVELOPMENT_MODE=True  

# Define a dictionary mapping status values to their descriptions
STATUS_DESCRIPTIONS = {
    1: 'Cancelled',
    2: 'Traded / Filled',
    3: 'For future use',
    4: 'Transit',
    5: 'Rejected',
    6: 'Pending',
}


FYERS_APP_ID="H9O406XBXW-100"
FYERS_SECRET_ID="XOVF82L85V"
FYERS_REDIRECT_URL="https://cc7e-2405-201-f007-4977-d0-2c0b-866a-38ba.ngrok-free.app"


if not DEVELOPMENT_MODE:
    #for production
    # FYERS_APP_ID="5NYKD87NTH-100"
    # FYERS_SECRET_ID="XIXJN6AKI5"
    # FYERS_REDIRECT_URL="https://tradewithappz.co.in"

    FYERS_APP_ID="4CIPNEEHU0-100"
    FYERS_SECRET_ID="6BF3KJFCID"
    FYERS_REDIRECT_URL="https://tradewithappz.onrender.com"

DEFAULT_BROKERAGE=40

TIME_ZONE = 'Asia/Kolkata'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'scheduler': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
