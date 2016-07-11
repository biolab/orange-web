"""
Django settings for orange_web project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os
import socket

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SCREENSHOTS_DIR = \
    os.path.join(BASE_DIR, 'homepage', 'static', 'homepage', 'screenshots')
SCREENSHOTS_INDEX = os.path.join(SCREENSHOTS_DIR, 'screenshots.xml')
LICENSE_FILE = os.path.join(BASE_DIR, 'LICENSES')

# Quick-getting_started development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = 'input a random string'
RECAPTCHA_SECRET = 'get the string from Google'

# SECURITY WARNING: don't run with debug turned on in production!
# FOR TESTING WHEN FALSE: python manage.py runserver --insecure

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['orange.biolab.si', 'new.orange.biolab.si']

BLOG_HOST = 'blog.biolab.si'

# EMAIL BACKEND publishes mail send by send_mail() function to standard output.
# To change behavior for production, you will have to set up the SMTP BACKEND.
# Please refer to documentation:
# https://docs.djangoproject.com/en/1.6/topics/email/

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'homepage'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'orange_web.urls'

WSGI_APPLICATION = 'orange_web.wsgi.application'

ADMINS = (
    ('Info', 'info@biolab.si'),
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

if socket.gethostname() == 'biolab':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'orange_website',
            'USER': 'orange_website',
        }
    }

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
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
DOWNLOAD_DIR = os.path.abspath("./download")
DOWNLOAD_SET_PATTERN = os.path.join(DOWNLOAD_DIR, "filenames_%s.set")
WIDGET_CATALOG = os.path.abspath("./homepage/static/widgets.json")
FEATURES_CATALOG = os.path.abspath("./homepage/static/features.json")
TESTIMONIALS_CATALOG = os.path.abspath("./homepage/static/testimonials.json")

# A custom context processor
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'orange_web.processors.get_current_page',
)
