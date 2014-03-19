import os
import dj_database_url
from configurations import Configuration


class Dev(Configuration):
  BASE_DIR = os.path.dirname(os.path.dirname(__file__))

  # Quick-start development settings - unsuitable for production
  # See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

  # SECURITY WARNING: keep the secret key used in production secret!
  SECRET_KEY = 'h=q7k_ieod06s=ng20r(mky1qc5jwy%c$d(-^9&v)0&_g4rg(r'

  # Application definition

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

  # Internationalization
  # https://docs.djangoproject.com/en/1.6/topics/i18n/

  LANGUAGE_CODE = 'en-us'

  TIME_ZONE = 'UTC'

  USE_I18N = True

  USE_L10N = True

  USE_TZ = True


  # Static files (CSS, JavaScript, Images)
  # https://docs.djangoproject.com/en/1.6/howto/static-files/

  STATIC_URL = '/static/'

  TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
  )

  LOGIN_REDIRECT_URL = '/'

  DEBUG = True

  TEMPLATE_DEBUG = True

  ALLOWED_HOSTS = ['*']

  ACCOUNT_ACTIVATION_DAYS = 7
  AUTH_USER_EMAIL_UNIQUE = True
  EMAIL_HOST = 'localhost'
  EMAIL_PORT = 1025
  EMAIL_HOST_USER = ''
  EMAIL_HOST_PASSWORD = ''
  EMAIL_USE_TLS = False
  DEFAULT_FROM_EMAIL = 'stagings@example.com'

  # Database
  # https://docs.djangoproject.com/en/1.6/ref/settings/#databases

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


class Prod(Configuration):
  BASE_DIR = os.path.dirname(os.path.dirname(__file__))

  # Quick-start development settings - unsuitable for production
  # See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

  # SECURITY WARNING: keep the secret key used in production secret!
  SECRET_KEY = 'h=q7k_ieod06s=ng20r(mky1qc5jwy%c$d(-^9&v)0&_g4rg(r'

  # Application definition

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

  # Internationalization
  # https://docs.djangoproject.com/en/1.6/topics/i18n/

  LANGUAGE_CODE = 'en-us'

  TIME_ZONE = 'UTC'

  USE_I18N = True

  USE_L10N = True

  USE_TZ = True


  # Static files (CSS, JavaScript, Images)
  # https://docs.djangoproject.com/en/1.6/howto/static-files/

  STATIC_URL = '/static/'

  TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
  )

  LOGIN_REDIRECT_URL = '/'

  ALLOWED_HOSTS = ['*']

  ACCOUNT_ACTIVATION_DAYS = 7
  AUTH_USER_EMAIL_UNIQUE = True
  EMAIL_HOST = 'localhost'
  EMAIL_PORT = 1025
  EMAIL_HOST_USER = ''
  EMAIL_HOST_PASSWORD = ''
  EMAIL_USE_TLS = False
  DEFAULT_FROM_EMAIL = 'stagings@example.com'

  # Database
  # https://docs.djangoproject.com/en/1.6/ref/settings/#databases

  DEBUG = False

  TEMPLATE_DEBUG = False
  DATABASES = {
    'default': dj_database_url.config()
  }

  SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
  STATIC_ROOT = 'staticfiles'

  STATICFILES_DIRS = (
      os.path.join(BASE_DIR, 'static'),
  )
