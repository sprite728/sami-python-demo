"""
Django settings for python project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SWAGGER_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
SWAGGER_API = os.path.join(SWAGGER_BASE_DIR, 'swagger')
sys.path.insert(0, os.path.join(SWAGGER_API , "python") )

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')9lgw*m+*@)#)(wc)_6lnu((uvgx8#cbkwoi*wgt%cs1!oaj-t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sami',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'python.urls'

WSGI_APPLICATION = 'python.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
TEMPLATE_DIRS = (
    TEMPLATE_PATH,
)

SAMI_SERVER_URL = "https://api.samsungsami.io/v1.1"  #sami server base url
SAMI_ACCOUNT_SERVER_URL = "https://accounts.samsungsami.io" #sami account server, needed for oauth login
SAMI_ACCOUNT_TOKEN = "https://accounts.samsungsami.io/authorize?" #sami first oauth url. Call this to retrieve the code
SAMI_ACCOUNT_ACCESS_TOKEN = "https://accounts.samsungsami.io/token" #sami second oauth url. Call this to retrieve the access token
SAMI_RETURN_URI = "http://localhost:8000/users/authorized" #local return url, the oauth will redirect to this url

CLIENT_ID = "<YOUR CLIENT ID>"
CLIENT_SECRET = "<YOUR CLIENT SECRET>";
LOGIN_URL = "/login_required" #django redirectd to this url when the user attemps to go to a page that needs login but the user is logged out
