"""
Django settings for goshop project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--i)jgqjqpg3b6ehf#-b8i8o%mdq+un3j!z(ynlt&0n2pdo+gsx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

SHARED_APPS = (
    'tenant_schemas',  # mandatory, should always be before any django app
    'customers',  # you must list the app where your tenant model resides in
    'django.contrib.contenttypes',
    'onboarding',
    # everything below here is optional
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'products',
    'django_extensions'
)

TENANT_APPS = (
    'django.contrib.contenttypes',
    'payment',
    'onboarding',
    'products',
    'rest_framework',
    'restapis',
    'basket',
    'dashboard',
    'orders',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django_elasticsearch_dsl'
)

INSTALLED_APPS = [
    'tenant_schemas',
    'customers',
    'onboarding',
    'products',
    'rest_framework',
    'restapis',
    'basket',
    'dashboard',
    'orders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'payment',
    'django_extensions',
    'django_elasticsearch_dsl',

]

MIDDLEWARE = [
    'tenant_schemas.middleware.TenantMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'basket.middleware.CustomBasketMiddleware'
]

CSRF_TRUSTED_ORIGINS = ['*']

ROOT_URLCONF = 'goshop.urls'
PUBLIC_SCHEMA_URLCONF = 'goshop.urls'
SHOW_PUBLIC_IF_NO_TENANT_FOUND = True

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
            ],
        },
    },
]

WSGI_APPLICATION = 'goshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
        'default': {
            'ENGINE': 'tenant_schemas.postgresql_backend',
            'NAME': os.environ.get("DBNAME"),
            'USER': os.environ.get("DBUSER"),
            'PASSWORD': os.environ.get("DBPASSWORD"),
            'HOST': os.environ.get("DBHOST"),
            'PORT': 5432,
        }
    }

DATABASE_ROUTERS = (
    'tenant_schemas.routers.TenantSyncRouter',
)

TENANT_MODEL = "customers.Client"

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles")
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PUBLIC_DOMAIN_URL = os.environ.get("PUBLIC_DOMAIN_URL")
GO_DADDY_API_KEY = os.environ.get("GO_DADDY_API_KEY")
GO_DADDY_API_SECRET = os.environ.get("GO_DADDY_API_SECRET")


STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")

STRIPE_CONNECT_CLIENT_ID = os.environ.get("STRIPE_CONNECT_CLIENT_ID")
IS_PRODUCTION = bool(int(os.environ.get("IS_PRODUCTION", "1")))


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

if IS_PRODUCTION:
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': os.environ.get("CLOUDINARY_CLOUD_NAME"),
        'API_KEY': os.environ.get("CLOUDINARY_API_KEY"),
        'API_SECRET': os.environ.get("CLOUDINARY_API_SECRET"),
    }
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


ORDER_NUMBERING_FROM = 10000
LOGOUT_REDIRECT_URL = '/'

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200'
    },
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

LOGIN_URL = '/customer/login/'
