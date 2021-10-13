"""
Django settings for meteosangue project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os, sys

VERSION = '1.2.0'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if os.getenv('PRODUCTION', '0') == '1' else True

ALLOWED_HOSTS = ['*']

SECRET_KEY = os.getenv('SECRET_KEY', 'S3KR3TK3Y_D3V')

FETCH_SITE_WAIT = int(os.getenv('FETCH_SITE_WAIT', 20))

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', 'D3V')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET', 'D3V')
CONSUMER_KEY = os.getenv('CONSUMER_KEY', 'D3V')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET', 'D3V')

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'D3V')
TELEGRAM_CHANNEL = os.getenv('TELEGRAM_CHANNEL', 'D3V')

FACEBOOK_TOKEN = os.getenv('FACEBOOK_TOKEN', 'D3V')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'api',
    'huey.contrib.djhuey',
    'rest_framework',
    'rest_framework.authtoken'
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

ROOT_URLCONF = 'meteosangue.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'meteosangue.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'meteosangue.sqlite3'),
        },
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.environ.get('SQLITE_PATH', os.path.join(BASE_DIR, 'db.sqlite3')),
        },
    }


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Blood associations data

BLOOD_ASSOCIATIONS = [

    {
        'name': 'Avis Nazionale',
        'twitter_id': '@avisnazionale',
        'facebook_id': '154932917976132'
    },

    {
        'name': 'Avis Giovani',
        'twitter_id': '@giovaniavis',
    },

    {
        'name': 'Fidas Nazionale',
        'twitter_id': '@FIDASnazionale',
        'facebook_id': '49816054736'
    },

    {
        'name': 'Frates Nazionale',
        'twitter_id': '@FratresNaz',
    },

    {
        'name': 'Centro Naz. Sangue',
        'twitter_id': '@CentroSangue',
        'facebook_id': '477808612320970'
    }

]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

ENV_PATH = os.path.abspath(os.path.dirname(__file__))
UPLOAD_ROOT = os.path.join(ENV_PATH, 'uploads/')
UPLOAD_METEO = 'meteo'

BLOOD_FETCH_INTERVAL = 60 * 15


import dj_database_url
db_from_env = dj_database_url.config()

from huey import RedisHuey
from redis import ConnectionPool

pool = ConnectionPool(
    host=os.getenv('REDIS_URL', 'localhost'),
    port=6379,
    max_connections=20
)
HUEY = RedisHuey('meteosanguequeue', connection_pool=pool)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

if db_from_env:
    DATABASES['default'].update(db_from_env)

if 'test' in sys.argv:
    try:
        from .test_settings import *
    except ImportError:
        pass

