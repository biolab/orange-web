"""
Django settings for orange_web project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCREENSHOTS_DIR = \
    os.path.join(BASE_DIR, 'homepage', 'static', 'homepage', 'screenshots')
SCREENSHOTS_INDEX = os.path.join(SCREENSHOTS_DIR, 'screenshots.xml')
LICENSE_FILE = os.path.join(BASE_DIR, 'LICENSES')

# Quick-getting_started development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get(
    "SECRET_KEY", 'input a random string')
RECAPTCHA_SECRET = os.environ.get(
    "RECAPTCHA_SECRET", 'get the string from Google')

# SECURITY WARNING: don't run with debug turned on in production!
# FOR TESTING WHEN FALSE: python manage.py runserver --insecure

DEBUG = os.environ.get("DEBUG", "True") in ["True", "1"]

ALLOWED_HOSTS = []

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
    'homepage',
    'courses',
    'download',
    'error_report',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'orange_web.urls'

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
            'debug': True,
        },
    },
]

WSGI_APPLICATION = 'orange_web.wsgi.application'

ADMINS = (
    ('Info', 'info@biolab.si'),
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'local.db'),
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
DOWNLOAD_DIR = os.environ.get(
    "DOWNLOAD_DIR", os.path.abspath("./download"))
DOWNLOAD_SET_PATTERN = os.environ.get(
    "DOWNLOAD_SET_PATTERN", os.path.join(DOWNLOAD_DIR, "filenames_%s.set"))
WIDGET_CATALOG = os.environ.get(
    "WIDGET_CATALOG", os.path.abspath("./homepage/static/widgets.json"))
ADDON_WIDGET_CATALOG = os.environ.get(
    "ADDON_WIDGET_CATALOG", os.path.abspath("./homepage/static/"))
FEATURES_CATALOG = os.environ.get(
    "FEATURES_CATALOG", os.path.abspath("./homepage/static/features.json"))
TESTIMONIALS_CATALOG = os.environ.get(
    "TESTIMONIALS_CATALOG", os.path.abspath("./homepage/static/testimonials.json"))

# Error report settings
ERROR_REPORT_DIR = os.environ.get(
    "ERROR_REPORT_DIR", os.path.abspath("./error_report/"))
# Biolab's testing Sentry project
ERROR_REPORT_SENTRY_DSN_ORANGE = 'https://261797e8fa4544ffb931bc495157d2e3:44e30b93f9f1463a975725f82ca18039@sentry.io/128442'

# Log errors in dev to console only
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
        'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
    },
}
