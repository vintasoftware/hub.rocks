"""
Django settings for hubrocks project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os
import re
from decouple import config, Csv
import dj_database_url
import sys
TEST = 'test' in sys.argv

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def base_dir_join(*args):
    return os.path.join(BASE_DIR, *args)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='egw%de7grf@4+)l9hs41rk7+cp$0pj7l*@l@3+=v^h#yii_5@!')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)
LOCAL = config('LOCAL', default=True, cast=bool)
TEMPLATE_DEBUG = config('TEMPLATE_DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())


# Admins and Managers
ADMINS = (
    ('Vinta', 'contato@vinta.com.br'),
    ('Andre', 'andre@vinta.com.br'),
)
MANAGERS = ADMINS

AUTH_USER_MODEL = 'accounts.Account'

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'collectfast',  # must be before 'staticfiles'
    'django.contrib.staticfiles',
    'compressor',
    'storages',
    'djangobower',
    'rest_framework',
    'widget_tweaks',

    'core',
    'tracks',
    'player',
    'accounts',
)

BOWER_INSTALLED_APPS = (
    'bootstrap-sass-official#3.3.3',
    'selectize#0.11.2',
    'https://github.com/wayneashleyberry/selectize-enter-key-submit.git',
    'jquery#2.1.3',
    'angular#1.3.13',
    'https://github.com/grevory/angular-local-storage.git#0.1.5',
    'https://github.com/monicao/angular-uuid4.git#v0.2.0',
    'faye#1.1.0',
    'angular-faye#0.2.2',
    'jquery-cookie#1.4.1',
)
BOWER_COMPONENTS_ROOT = base_dir_join('components')

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',

    'core.context_processors.fanout_realm',
    'core.context_processors.youtube_key',
)

ROOT_URLCONF = 'hubrocks.urls'

WSGI_APPLICATION = 'hubrocks.wsgi.application'

IGNORABLE_404_URLS = (
    re.compile(r'^/api/.+$'),
)


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(
        env='DATABASE_URL', default='sqlite:///' + base_dir_join('db.sqlite3'))
}


# Caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'collectfast': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'django_db_cache_collectfast',
        'TIMEOUT': 60 * 60 * 24 * 7 * 30,  # 1 month
        'OPTIONS': {
            'MAX_ENTRIES': 10000
        }
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# django rest framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'djangobower.finders.BowerFinder',
    'compressor.finders.CompressorFinder',
)

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default=None)
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default=None)
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default=None)
AWS_S3_SECURE_URLS = False
AWS_QUERYSTRING_AUTH = False
AWS_S3_CUSTOM_DOMAIN = '{0}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)

STATICFILES_STORAGE = config('STATICFILES_STORAGE', 'django.contrib.staticfiles.storage.StaticFilesStorage')
DEFAULT_FILE_STORAGE = config('DEFAULT_FILE_STORAGE', 'django.core.files.storage.FileSystemStorage')
MEDIA_ROOT = base_dir_join('media')
STATIC_ROOT = base_dir_join('staticfiles')

if LOCAL:
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
else:
    STATIC_URL = 'http://{0}/static/'.format(AWS_S3_CUSTOM_DOMAIN)
    MEDIA_URL = 'http://{0}/media/'.format(AWS_S3_CUSTOM_DOMAIN)


# collectfast
AWS_PRELOAD_METADATA = True
COLLECTFAST_CACHE = 'collectfast'
COLLECTFAST_ENABLED = not LOCAL


# django-compressor
COMPRESS_ENABLED = config('COMPRESS_ENABLED', default=False)
COMPRESS_STORAGE = STATICFILES_STORAGE
COMPRESS_URL = STATIC_URL

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'core.compressor_filters.PatchedSCSSCompiler'),
)

COMPRESS_CSS_FILTERS = [
    'core.compressor_filters.CustomCssAbsoluteFilter',
]


# Email settings
DEFAULT_FROM_EMAIL = 'info@lotebox.com'

if LOCAL:
    INSTALLED_APPS += ('naomi',)
    EMAIL_BACKEND = 'naomi.mail.backends.naomi.NaomiBackend'
    EMAIL_FILE_PATH = base_dir_join('tmp_email')
else:
    SERVER_EMAIL = config('SERVER_EMAIL')
    EMAIL_HOST = config('EMAIL_HOST')
    EMAIL_PORT = config('EMAIL_PORT')
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

TEMPLATED_EMAIL_TEMPLATE_DIR = 'emails/'
TEMPLATED_EMAIL_FILE_EXTENSION = 'email'


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'segment': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        }
    }
}


if TEST:
    import logging
    logging.disable(logging.INFO)

FANOUT_REALM = config('FANOUT_REALM', default=None)
FANOUT_KEY = config('FANOUT_KEY', default=None)


LASTFM_API_KEY = config('LASTFM_API_KEY', default=None)
LASTFM_API_SECRET = config('LASTFM_API_SECRET', default=None)

# Make sure it's a public API access key (Key for browser applications)
YOUTUBE_KEY = config('YOUTUBE_KEY', default=None)
