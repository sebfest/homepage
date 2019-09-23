import os

from django.utils import timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from .credential import SECRET_KEY
SECRET_KEY = SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#Hosts
ALLOWED_HOSTS = ['127.0.0.1', '.pythonanywhere.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    #Third party apps
    'disqus',
    'markdownx',
    'bootstrap4',
    'tagulous',

    #My apps
    'blog.apps.BlogConfig',
    'research.apps.ResearchConfig',
    'teaching.apps.TeachingConfig',
    'contact.apps.ContactConfig',
]

if DEBUG is True:
    INSTALLED_APPS += ['debug_toolbar',]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'homepage.urls'

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

WSGI_APPLICATION = 'homepage.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
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

#User model
AUTH_USER_MODEL = 'auth.User'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Django sites
SITE_ID = 1

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media files (.jpg, .pdf)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Markdownx settings
MARKDOWNX_MARKDOWN_EXTENSIONS = [
    'extra',
]
MARKDOWNX_MEDIA_PATH = timezone.now().strftime('markdownx/%Y/%m/%d')
MARKDOWNX_IMAGE_MAX_SIZE = {
    'size': (1920, 1080),
    'quality': 90
}

# Bootstrap4
BOOTSTRAP4 = {
    'include_jquery': True,
}

#Disquss
from .disqus_info import *

DISQUS_API_KEY = DISQUS_API_KEY
DISQUS_WEBSITE_SHORTNAME = DISQUS_WEBSITE_SHORTNAME

#Email configuration
from .email_info import *

EMAIL_BACKEND = EMAIL_BACKEND
EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_PORT = EMAIL_PORT
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Debug toolbar
INTERNAL_IPS = ALLOWED_HOSTS

#Tagolous
SERIALIZATION_MODULES = {
    'xml':    'tagulous.serializers.xml_serializer',
    'json':   'tagulous.serializers.json',
    'python': 'tagulous.serializers.python',
    'yaml':   'tagulous.serializers.pyyaml',
}