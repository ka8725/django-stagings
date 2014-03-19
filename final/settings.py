import os
import dj_database_url
from configurations import Configuration

class Base(Configuration):
  BASE_DIR = os.path.dirname(os.path.dirname(__file__))

  SECRET_KEY = 'h=q7k_ieod06s=ng20r(mky1qc5jwy%c$d(-^9&v)0&_g4rg(r'
  INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'braces',
    'registration',
    'stagings',
    )

  MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
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
    'stagings.context_processors.last_commit_date',
    'stagings.context_processors.is_courier',
    )

  ROOT_URLCONF = 'final.urls'

  WSGI_APPLICATION = 'final.wsgi.application'

  LANGUAGE_CODE = 'en-us'

  TIME_ZONE = 'UTC'

  USE_I18N = True

  USE_L10N = True

  USE_TZ = True

  STATIC_URL = '/static/'

  LOGIN_REDIRECT_URL = '/'
  ALLOWED_HOSTS = ['*']

  ACCOUNT_ACTIVATION_DAYS = 7
  AUTH_USER_EMAIL_UNIQUE = True
  STATIC_ROOT = 'staticfiles'


class Dev(Base):
  DEBUG = True

  TEMPLATE_DEBUG = True

  EMAIL_HOST = 'localhost'
  EMAIL_PORT = 1025
  EMAIL_HOST_USER = ''
  EMAIL_HOST_PASSWORD = ''
  EMAIL_USE_TLS = False
  DEFAULT_FROM_EMAIL = 'stagings@example.com'

  DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
      'NAME': 'final',
      'HOST': '127.0.0.1',
      'USERNAME': 'ka8725',
      'PORT': '5432',
      'PASSWORD': '',
      'ATOMIC_REQUEST': True,
    }
  }


class Prod(Base):
  EMAIL_HOST = 'smtp.sendgrid.net'
  EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME', '')
  EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD', '')
  EMAIL_PORT = 25
  EMAIL_USE_TLS = False
  DEFAULT_FROM_EMAIL = 'heroku@stagings.com'

  DEBUG = False

  TEMPLATE_DEBUG = False
  DATABASES = {
    'default': dj_database_url.config()
  }

  SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
